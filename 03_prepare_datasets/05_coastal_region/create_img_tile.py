from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.vectorutils
import rsgislib.rastergis

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        gadm_dist_img = os.path.join(self.params['tmp_dir'], "{}_gadm_dist_img.kea".format(self.params['tile']))
        rsgislib.imagecalc.calcDist2ImgVals(self.params['gadm_img'], gadm_dist_img, [1], valsImgBand=1, gdalformat='KEA', maxDist=200, noDataVal=201, unitGEO=False)

        gadm_inv_dist_img = os.path.join(self.params['tmp_dir'], "{}_gadm_inv_dist_img.kea".format(self.params['tile']))
        rsgislib.imagecalc.calcDist2ImgVals(self.params['inv_gadm_img'], gadm_inv_dist_img, [1], valsImgBand=1, gdalformat='KEA', maxDist=300, noDataVal=301, unitGEO=False)

        band_defns = [rsgislib.imagecalc.BandDefn('dland', gadm_dist_img, 1),
                      rsgislib.imagecalc.BandDefn('docean', gadm_inv_dist_img, 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], '(dland < 100) && (docean < 100)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "gadm_img", "inv_gadm_img", "out_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


