from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.tools.utils
import rsgislib.imageutils
import rsgislib.imageregistration


logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        offsets = rsgislib.imageregistration.findImageOffset(self.params['sar_ref_img'], self.params['sar_flt_buf_img'], [1, 2, 3], [1, 2, 3], rsgislib.imageregistration.METRIC_CORELATION, 3, 3, 10)

        img_res_x, img_res_y = rsgislib.imageutils.getImageRes(self.params['sar_flt_buf_img'], abs_vals=True)

        sp_off_x = offsets[0] * img_res_x
        sp_off_y = offsets[1] * img_res_y

        rsgislib.imageregistration.applyOffset2Image(self.params['sar_flt_buf_img'], self.params['out_flt_buf_img'], 'KEA', rsgislib.TYPE_16INT, sp_off_x, sp_off_y)

        rsgislib.imageutils.resampleImage2Match(self.params['sar_ref_img'], self.params['out_flt_buf_img'], self.params['out_rsmpld_img'], 'KEA', 'cubic', rsgislib.TYPE_16INT, 32767)
        rsgislib.imageutils.popImageStats(self.params['out_rsmpld_img'], True, 32767, True)

        out_offs = dict()
        out_offs['tile'] = self.params['tile']
        out_offs['x_pxl_off'] = float(offsets[0])
        out_offs['y_pxl_off'] = float(offsets[1])
        out_offs['x_spl_off'] = float(sp_off_x)
        out_offs['y_spl_off'] = float(sp_off_y)
        rsgislib.tools.utils.writeDict2JSON(out_offs, self.params['out_off_json'])


    def required_fields(self, **kwargs):
        return ["tile", "sar_ref_img", "sar_flt_buf_img", "out_flt_buf_img", "out_rsmpld_img", "out_off_json"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_flt_buf_img']] = 'gdal_image'
        files_dict[self.params['out_rsmpld_img']] = 'gdal_image'
        files_dict[self.params['out_off_json']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_flt_buf_img']):
            os.remove(self.params['out_flt_buf_img'])

        if os.path.exists(self.params['out_rsmpld_img']):
            os.remove(self.params['out_rsmpld_img'])

        if os.path.exists(self.params['out_off_json']):
            os.remove(self.params['out_off_json'])

if __name__ == "__main__":
    CreateImageTile().std_run()


