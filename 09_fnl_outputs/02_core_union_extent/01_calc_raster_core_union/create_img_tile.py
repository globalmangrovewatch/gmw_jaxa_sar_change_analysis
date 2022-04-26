from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib.imagecalc
import rsgislib.imageutils


logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        os.environ["RSGISLIB_IMG_CRT_OPTS_GTIFF"] = "TILED=YES:COMPRESS=LZW"

        rsgislib.imagecalc.calc_multi_img_band_stats(self.params['gmw_imgs'], self.params['out_union_img'], rsgislib.SUMTYPE_MAX, 'KEA', rsgislib.TYPE_8UINT, 0, False)
        rsgislib.imageutils.pop_thmt_img_stats(self.params['out_union_img'])
        clr_lut = dict()
        clr_lut[1] = '#009600'
        rsgislib.imageutils.define_colour_table(self.params['out_union_img'], clr_lut)

        rsgislib.imagecalc.calc_multi_img_band_stats(self.params['gmw_imgs'], self.params['out_core_img'], rsgislib.SUMTYPE_MIN, 'KEA', rsgislib.TYPE_8UINT, 0, False)
        rsgislib.imageutils.pop_thmt_img_stats(self.params['out_core_img'])
        clr_lut = dict()
        clr_lut[1] = '#009600'
        rsgislib.imageutils.define_colour_table(self.params['out_core_img'], clr_lut)

    def required_fields(self, **kwargs):
        return ["gmw_tile", "gmw_imgs", "out_union_img", "out_core_img"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_union_img']] = 'gdal_image'
        files_dict[self.params['out_core_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_union_img']):
            os.remove(self.params['out_union_img'])

        if os.path.exists(self.params['out_core_img']):
            os.remove(self.params['out_core_img'])

if __name__ == "__main__":
    CreateImageTile().std_run()


