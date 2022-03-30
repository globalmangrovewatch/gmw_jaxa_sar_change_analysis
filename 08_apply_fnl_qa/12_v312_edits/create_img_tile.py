from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc
import rsgislib.vectorutils
import rsgislib.vectorutils.createrasters

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        burn_v25_img = os.path.join(self.params['tmp_dir'], "{}_burn_v25_lyr.kea".format(self.params['tile']))
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(vec_file=self.params['burn_v25_vec_file'], vec_lyr=self.params['burn_v25_vec_lyr'],
                                                             input_img=self.params['gmw_tile'], output_img=burn_v25_img, gdalformat='KEA', burn_val=1,
                                                             datatype=rsgislib.TYPE_8UINT)

        burn_v25_count = rsgislib.imagecalc.count_pxls_of_val(burn_v25_img, vals=[1])[0]

        rm_mng_img = os.path.join(self.params['tmp_dir'], "{}_rm_mng_lyr.kea".format(self.params['tile']))
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(vec_file=self.params['rm_mng_vec_file'], vec_lyr=self.params['rm_mng_vec_lyr'],
                                                             input_img=self.params['gmw_tile'], output_img=rm_mng_img, gdalformat='KEA', burn_val=1,
                                                             datatype=rsgislib.TYPE_8UINT)
        rm_mng_count = rsgislib.imagecalc.count_pxls_of_val(rm_mng_img, vals=[1])[0]


        if (burn_v25_count > 0) and (rm_mng_count > 0):
            band_defns = [
                rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                rsgislib.imagecalc.BandDefn('v25', self.params['gmw_v25_img'], 1),
                rsgislib.imagecalc.BandDefn('burn', burn_v25_img, 1),
                rsgislib.imagecalc.BandDefn('rm', rm_mng_img, 1)]
            rsgislib.imagecalc.band_math(self.params['out_img'], '(burn==1)&&(v25==1)?1:gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        elif burn_v25_count > 0:
            band_defns = [
                rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                rsgislib.imagecalc.BandDefn('v25', self.params['gmw_v25_img'], 1),
                rsgislib.imagecalc.BandDefn('burn', burn_v25_img, 1)]
            rsgislib.imagecalc.band_math(self.params['out_img'], '(burn==1)&&(v25==1)?1:gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        elif rm_mng_count > 0:
            band_defns = [
                rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                rsgislib.imagecalc.BandDefn('rm', rm_mng_img, 1)]
            rsgislib.imagecalc.band_math(self.params['out_img'], '(rm==1)?0:gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        else:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1)]
            rsgislib.imagecalc.band_math(self.params['out_img'], 'gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        rsgislib.rastergis.pop_rat_img_stats(self.params['out_img'], add_clr_tab=True, calc_pyramids=True, ignore_zero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "burn_v25_vec_file", "burn_v25_vec_lyr", "rm_mng_vec_file", "rm_mng_vec_lyr", "gmw_v25_img", "out_img", "tmp_dir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


