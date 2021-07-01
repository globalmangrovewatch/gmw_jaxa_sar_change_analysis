from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        out_stats = dict()
        out_stats['mng_chng'] = 0
        out_stats['nmng_chng'] = 0
        out_stats['mng_chng_uncertain'] = []
        out_stats['nmng_chng_uncertain'] = []

        if os.path.exists(self.params['mng_chng_img']):
            out_stats['mng_chng'] = rsgislib.imagecalc.countPxlsOfVal(self.params['mng_chng_img'], vals=[1])[0]

        if os.path.exists(self.params['nmng_chng_img']):
            out_stats['nmng_chng'] = rsgislib.imagecalc.countPxlsOfVal(self.params['nmng_chng_img'], vals=[1])[0]

        if os.path.exists(self.params['mng_chng_uncertain_img']):
            pxl_counts = rsgislib.imagecalc.countPxlsOfVal(self.params['mng_chng_uncertain_img'], vals=[1,2,3,4,5,6,7,8,9,10,11,12])
            culm_pxl_count = []
            culm_sum = 0
            for pxl_count in pxl_counts:
                culm_sum = culm_sum + pxl_count
                culm_pxl_count.append(culm_sum)
            out_stats['mng_chng_uncertain'] = culm_pxl_count

        if os.path.exists(self.params['nmng_chng_uncertain']):
            pxl_counts = rsgislib.imagecalc.countPxlsOfVal(self.params['nmng_chng_uncertain'], vals=[1,2,3,4,5,6,7,8,9,10,11,12])
            culm_pxl_count = []
            culm_sum = 0
            for pxl_count in pxl_counts:
                culm_sum = culm_sum + pxl_count
                culm_pxl_count.append(culm_sum)
            out_stats['nmng_chng_uncertain'] = culm_pxl_count

        rsgis_utils = rsgislib.RSGISPyUtils()
        rsgis_utils.writeDict2JSON(out_stats, self.params['out_stats_file'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "mng_chng_img", "nmng_chng_img", "mng_chng_uncertain_img", "nmng_chng_uncertain_img", "out_stats_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_stats_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_stats_file']):
            os.remove(self.params['out_stats_file'])

if __name__ == "__main__":
    CreateImageTile().std_run()


