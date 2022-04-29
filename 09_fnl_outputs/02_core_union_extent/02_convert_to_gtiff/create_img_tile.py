from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()
        rsgislib.imagecalc.image_math(self.params['gmw_tile'], self.params['out_img'], 'b1', 'GTIFF', rsgislib.TYPE_8UINT)
        rsgislib.imageutils.pop_thmt_img_stats(self.params['out_img'])
        clr_lut = dict()
        clr_lut[1] = '#009600'
        rsgislib.imageutils.define_colour_table(self.params['out_img'], clr_lut)

    def required_fields(self, **kwargs):
        return ["gmw_tile", "out_img"]


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


