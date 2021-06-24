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
        os.environ["RSGISLIB_IMG_CRT_OPTS_GTIFF"] = "TILED=YES:COMPRESS=LZW"

        rsgislib.imagecalc.calcMultiImgBandStats(self.params['gmw_tiles'], self.params['out_core_img'], rsgislib.SUMTYPE_MIN, 'GTIFF', rsgislib.TYPE_8UINT, 0, False)
        rsgislib.imageutils.popImageStats(self.params['out_core_img'], usenodataval=True, nodataval=0, calcpyramids=True)

        rsgislib.imagecalc.calcMultiImgBandStats(self.params['gmw_tiles'], self.params['out_union_img'], rsgislib.SUMTYPE_MAX, 'GTIFF', rsgislib.TYPE_8UINT, 0, False)
        rsgislib.imageutils.popImageStats(self.params['out_union_img'], usenodataval=True, nodataval=0, calcpyramids=True)

    def required_fields(self, **kwargs):
        return ["tile", "gmw_tiles", "out_core_img", "out_union_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_core_img']] = 'gdal_image'
        files_dict[self.params['out_union_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_core_img']):
            os.remove(self.params['out_core_img'])
        if os.path.exists(self.params['out_union_img']):
            os.remove(self.params['out_union_img'])

if __name__ == "__main__":
    CreateImageTile().std_run()


