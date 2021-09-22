from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imageutils
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):

        rsgislib.imagecalc.calcMultiImgBandStats(self.params['mng_ext_imgs'], self.params['out_gmw_mng_sum_img'], rsgislib.SUMTYPE_SUM, 'GTIFF', rsgislib.TYPE_8UINT, 0.0, True)
        rsgislib.imageutils.popImageStats(self.params['out_gmw_mng_sum_img'], True, 0, True)

    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "mng_ext_imgs", "out_gmw_mng_sum_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_gmw_mng_msk']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_gmw_mng_msk']):
            os.remove(self.params['out_gmw_mng_msk'])

if __name__ == "__main__":
    CreateImageTile().std_run()


