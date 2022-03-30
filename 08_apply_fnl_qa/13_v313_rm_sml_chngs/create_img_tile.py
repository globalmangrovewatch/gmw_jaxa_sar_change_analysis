from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])


        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


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


