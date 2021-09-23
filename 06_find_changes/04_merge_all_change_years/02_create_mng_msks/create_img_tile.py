from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imagecalc.imageMath(self.params['gmw_sum_tile'], self.params['out_gmw_mng_mjr_ext_img'], 'b1>5?1:0', 'KEA', rsgislib.TYPE_8UINT)
        rsgislib.rastergis.populateStats(self.params['out_gmw_mng_mjr_ext_img'], True, True, True)

        rsgislib.imagecalc.imageMath(self.params['gmw_sum_tile'], self.params['out_gmw_mng_max_ext_img'], 'b1>0?1:0', 'KEA', rsgislib.TYPE_8UINT)
        rsgislib.rastergis.populateStats(self.params['out_gmw_mng_max_ext_img'], True, True, True)

        rsgislib.imagecalc.imageMath(self.params['gmw_sum_tile'], self.params['out_gmw_mng_min_ext_img'], 'b1>9?1:0', 'KEA', rsgislib.TYPE_8UINT)
        rsgislib.rastergis.populateStats(self.params['out_gmw_mng_min_ext_img'], True, True, True)

    def required_fields(self, **kwargs):
        return ["tile", "gmw_sum_tile", "out_gmw_mng_mjr_ext_img", "out_gmw_mng_min_ext_img", "out_gmw_mng_max_ext_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_gmw_mng_mjr_ext_img']] = 'gdal_image'
        files_dict[self.params['out_gmw_mng_min_ext_img']] = 'gdal_image'
        files_dict[self.params['out_gmw_mng_max_ext_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_gmw_mng_mjr_ext_img']):
            os.remove(self.params['out_gmw_mng_mjr_ext_img'])

        if os.path.exists(self.params['out_gmw_mng_min_ext_img']):
            os.remove(self.params['out_gmw_mng_min_ext_img'])

        if os.path.exists(self.params['out_gmw_mng_max_ext_img']):
            os.remove(self.params['out_gmw_mng_max_ext_img'])

if __name__ == "__main__":
    CreateImageTile().std_run()


