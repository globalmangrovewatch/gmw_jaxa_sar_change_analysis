from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imageutils
import rsgislib.imageutils.imagelut

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imageutils.createBlankBufImgFromRefImg(self.params['sar_img'], self.params['out_img'], 'KEA', rsgislib.TYPE_16INT, buf_pxl_ext=50, buf_spt_ext=None, no_data_val=32767)

        scn_bbox = rsgislib.imageutils.getImageBBOX(self.params['out_img'])
        imgs = rsgislib.imageutils.imagelut.query_img_lut(scn_bbox, self.params['sar_tiles_lut_file'], self.params['sar_tiles_lut_lyr'])

        for img in imgs:
            print(img)

        if len(imgs) > 0:
            rsgislib.imageutils.includeImagesIndImgIntersect(self.params['out_img'], imgs)
            rsgislib.imageutils.popImageStats(input_img=self.params['out_img'], use_no_data=True, no_data_val=32767, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["tile", "sar_tiles_lut_file", "sar_tiles_lut_lyr", "sar_img", "out_img"]


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


