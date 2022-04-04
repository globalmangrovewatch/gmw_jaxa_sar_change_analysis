import numpy
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.rastergis
import rsgislib.segmentation

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        years = ['2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']

        exp = """(base==1)&&(chng==1)?1:
                 (base==0)&&(chng==0)?2:
                 (base==1)&&(chng==0)?3:
                 (base==0)&&(chng==1)?4:0
        """
        # 1 = Mangrove     - Mangrove
        # 2 = Not-Mangrove - Not-Mangrove
        # 3 = Mangrove     - Non-Mangrove
        # 4 = Non-Mangrove - Mangrove

        # Create the 1996 layer with small features removed...
        base_mng_img = self.params['gmw_tiles']['1996']
        tmp_1996_msk_img = os.path.join(self.params['tmp_dir'], "{}_1996_mng_msk.kea".format(self.params['tile']))
        rsgislib.imagecalc.image_math(base_mng_img, tmp_1996_msk_img, "b1==1?1:2", "KEA", rsgislib.TYPE_8UINT)

        # Clump the layer to find small features.
        tmp_1996_clumps_img = os.path.join(self.params['tmp_dir'], "{}_1996_clumps.kea".format(self.params['tile']))
        rsgislib.segmentation.clump(tmp_1996_msk_img, tmp_1996_clumps_img, "KEA", False, 0, False)
        rsgislib.rastergis.pop_rat_img_stats(clumps_img=tmp_1996_clumps_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)

        # Populate mangrove classification
        bs = [rsgislib.rastergis.BandAttStats(band=1, min_field='mngcls')]
        rsgislib.rastergis.populate_rat_with_stats(tmp_1996_msk_img, tmp_1996_clumps_img, bs)

        # Read Arrays
        mng_cls_arr = rsgislib.rastergis.get_column_data(tmp_1996_clumps_img, col_name="mngcls")
        histogram_arr = rsgislib.rastergis.get_column_data(tmp_1996_clumps_img, col_name="Histogram")

        # Define the classification.
        out_mng_cls_arr = numpy.zeros_like(mng_cls_arr, dtype=int)
        out_mng_cls_arr[(mng_cls_arr == 1)] = 1
        out_mng_cls_arr[(mng_cls_arr == 2)] = 0
        out_mng_cls_arr[(histogram_arr < 2) & (mng_cls_arr == 1)] = 0
        out_mng_cls_arr[(histogram_arr < 2) & (mng_cls_arr == 2)] = 1

        # Write classification to clumps.
        rsgislib.rastergis.set_column_data(clumps_img=tmp_1996_clumps_img, col_name="out_mng_cls", col_data=mng_cls_arr)

        # Export 1996 mangrove classification.
        out_mng_img = self.params['out_imgs']['1996']
        rsgislib.rastergis.export_col_to_gdal_img(tmp_1996_clumps_img, out_mng_img, "KEA", rsgislib.TYPE_8UINT, "out_mng_cls", rat_band=1)
        rsgislib.rastergis.pop_rat_img_stats(clumps_img=out_mng_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)
        base_mng_img = out_mng_img

        # Produce change years
        base_year = "1996"
        for chng_year in years:
            chng_mng_img = self.params['gmw_tiles'][chng_year]

            tmp_chngs_img = os.path.join(self.params['tmp_dir'], "{}_{}_{}_chngs.kea".format(self.params['tile'], base_year, chng_year))
            band_defns = list()
            band_defns.append(rsgislib.imagecalc.BandDefn('base', base_mng_img, 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('chng', chng_mng_img, 1))
            rsgislib.imagecalc.band_math(tmp_chngs_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.pop_rat_img_stats(clumps_img=tmp_chngs_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)

            tmp_chngs_clumps_img = os.path.join(self.params['tmp_dir'], "{}_{}_{}_chngs_clumps.kea".format(self.params['tile'], base_year, chng_year))
            rsgislib.segmentation.clump(tmp_chngs_img, tmp_chngs_clumps_img, "KEA", False, 0, False)
            rsgislib.rastergis.pop_rat_img_stats(clumps_img=tmp_chngs_clumps_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)

            bs = [rsgislib.rastergis.BandAttStats(band=1, min_field='chngcls')]
            rsgislib.rastergis.populate_rat_with_stats(tmp_chngs_img, tmp_chngs_clumps_img, bs)

            rsgislib.rastergis.calc_rel_border(tmp_chngs_clumps_img, "rel_bor_mng", "chngcls", "1", True)
            rsgislib.rastergis.calc_rel_border(tmp_chngs_clumps_img, "rel_bor_nmng", "chngcls", "2", True)

            chng_cls_arr = rsgislib.rastergis.get_column_data(tmp_chngs_clumps_img, col_name="chngcls")
            histogram_arr = rsgislib.rastergis.get_column_data(tmp_chngs_clumps_img, col_name="Histogram")
            rel_bor_mng_arr = rsgislib.rastergis.get_column_data(tmp_chngs_clumps_img, col_name="rel_bor_mng")
            rel_bor_nmng_arr = rsgislib.rastergis.get_column_data(tmp_chngs_clumps_img, col_name="rel_bor_nmng")

            mng_cls_arr = numpy.zeros_like(chng_cls_arr, dtype=int)
            # Copy the No Change Classes across
            mng_cls_arr[(chng_cls_arr == 1)] = 1
            mng_cls_arr[(chng_cls_arr == 2)] = 0
            # Where features larger than 2 pixels then assign
            # to the class clump has changed to.
            mng_cls_arr[(histogram_arr > 2) & (chng_cls_arr == 3)] = 0
            mng_cls_arr[(histogram_arr > 2) & (chng_cls_arr == 4)] = 1
            # Where features are <=2 pixels then assign to the class
            # the clump was in the base classification (i.e., no change).
            # if rel border to the previous class is > 0.5
            mng_cls_arr[(histogram_arr <= 2) & (chng_cls_arr == 3) & (rel_bor_mng_arr > 0.5)] = 1
            mng_cls_arr[(histogram_arr <= 2) & (chng_cls_arr == 4) & (rel_bor_nmng_arr > 0.5)] = 0
            # else if rel border to the previous class is < 0.5
            # then allow change.
            mng_cls_arr[(histogram_arr <= 2) & (chng_cls_arr == 3) & (rel_bor_mng_arr <= 0.5)] = 0
            mng_cls_arr[(histogram_arr <= 2) & (chng_cls_arr == 4) & (rel_bor_nmng_arr <= 0.5)] = 1

            # Write data to clumps.
            rsgislib.rastergis.set_column_data(clumps_img=tmp_chngs_clumps_img, col_name="mng_cls", col_data=mng_cls_arr)

            # Export mangrove to new image.
            out_mng_img = self.params['out_imgs'][chng_year]
            rsgislib.rastergis.export_col_to_gdal_img(tmp_chngs_clumps_img, out_mng_img, "KEA", rsgislib.TYPE_8UINT, "mng_cls", rat_band=1)
            rsgislib.rastergis.pop_rat_img_stats(clumps_img=out_mng_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)
            # Set as base classification for next iteration.
            base_mng_img = out_mng_img
            base_year = chng_year

        #if os.path.exists(self.params['tmp_dir']):
        #    shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tiles", "out_imgs", "tmp_dir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        for out_img in self.params['out_imgs']:
            files_dict[out_img] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        for out_img in self.params['out_imgs']:
            if os.path.exists(out_img):
                os.remove(out_img)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


