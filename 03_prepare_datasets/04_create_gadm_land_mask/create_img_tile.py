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

        rsgislib.vectorutils.rasteriseVecLyr(self.params['gadm_file'], self.params['gadm_lyr'], self.params['gmw_tile'],
                                             self.params['out_gadm_img'], gdalformat="KEA", burnVal=1,
                                             datatype=rsgislib.TYPE_8UINT, vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        rsgislib.imagecalc.imageMath(self.params['out_gadm_img'], self.params['out_inv_gadm_img'], "b1==1?0:1", "KEA", rsgislib.TYPE_8UINT)
        rsgislib.rastergis.populateStats(self.params['out_inv_gadm_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "gadm_file", "gadm_lyr", "out_gadm_img", "out_inv_gadm_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_gadm_img']] = 'gdal_image'
        files_dict[self.params['out_inv_gadm_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_gadm_img']):
            os.remove(self.params['out_gadm_img'])

        if os.path.exists(self.params['out_inv_gadm_img']):
            os.remove(self.params['out_inv_gadm_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


