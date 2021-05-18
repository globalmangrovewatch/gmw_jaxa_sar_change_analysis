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
        rsgislib.imagecalc.calcMultiImgBandStats(self.params['chng_imgs'], self.params['out_img'], rsgislib.SUMTYPE_MAX, 'KEA', rsgislib.TYPE_8UINT, 0, False)
        rsgislib.rastergis.populateStats(self.params['out_img'], True, True, True)


    def required_fields(self, **kwargs):
        return ["tile", "chng_imgs", "out_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

if __name__ == "__main__":
    CreateImageTile().std_run()


