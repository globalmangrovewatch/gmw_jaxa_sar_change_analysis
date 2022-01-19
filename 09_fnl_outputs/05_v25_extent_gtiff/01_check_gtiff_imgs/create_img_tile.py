from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.tools.utils

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):

        if os.path.exists(self.params['tif_img']):
            kea_pxl_count = rsgislib.imagecalc.count_pxls_of_val(self.params['gmw_tile'], vals=[1])
            tif_pxl_count = rsgislib.imagecalc.count_pxls_of_val(self.params['tif_img'], vals=[1])

            if kea_pxl_count[0] != tif_pxl_count[0]:
                os.remove(self.params['tif_img'])
            else:
                pxl_vals = dict()
                pxl_vals['kea'] = int(kea_pxl_count[0])
                pxl_vals['tif'] = int(tif_pxl_count[0])
                rsgislib.tools.utils.write_dict_to_json(pxl_vals, self.params['out_file'])

    def required_fields(self, **kwargs):
        return ["gmw_tile", "tif_img", "out_file"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

if __name__ == "__main__":
    CreateImageTile().std_run()


