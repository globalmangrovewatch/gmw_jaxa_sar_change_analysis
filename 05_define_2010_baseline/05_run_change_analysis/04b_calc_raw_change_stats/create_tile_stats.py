from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imagecalc


logger = logging.getLogger(__name__)


class CreateTileStats(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_vec_tile.py', descript=None)

    def do_processing(self, **kwargs):

        rsgis_utils = rsgislib.RSGISPyUtils()

        pxl_count_mng_2010 = rsgislib.imagecalc.countPxlsOfVal(self.params['img_2010_extent'], vals=[1])

        pxl_count_chng_mng = rsgislib.imagecalc.countPxlsOfVal(self.params['img_mng_chng_tile'], vals=[1])
        pxl_count_chng_nmng = rsgislib.imagecalc.countPxlsOfVal(self.params['img_nmng_chng_tile'], vals=[1])

        if self.params['calc_intervals']:
            pxl_count_chng_low_mng = rsgislib.imagecalc.countPxlsOfVal(self.params['img_mng_chng_lower_tile'], vals=[1])
            pxl_count_chng_low_nmng = rsgislib.imagecalc.countPxlsOfVal(self.params['img_nmng_chng_lower_tile'], vals=[1])

            pxl_count_chng_up_mng = rsgislib.imagecalc.countPxlsOfVal(self.params['img_mng_chng_upper_tile'], vals=[1])
            pxl_count_chng_up_nmng = rsgislib.imagecalc.countPxlsOfVal(self.params['img_nmng_chng_upper_tile'], vals=[1])

        stats_dict = dict()
        stats_dict['2010'] = int(pxl_count_mng_2010[0])
        stats_dict['chng_mng'] = int(pxl_count_chng_mng[0])
        stats_dict['chng_nmng'] = int(pxl_count_chng_nmng[0])
        if self.params['calc_intervals']:
            stats_dict['chng_low_mng'] = int(pxl_count_chng_low_mng[0])
            stats_dict['chng_low_nmng'] = int(pxl_count_chng_low_nmng[0])
            stats_dict['chng_up_mng'] = int(pxl_count_chng_up_mng[0])
            stats_dict['chng_up_nmng'] = int(pxl_count_chng_up_nmng[0])

        rsgis_utils.writeDict2JSON(stats_dict, self.params['out_file'])


    def required_fields(self, **kwargs):
        return ["img_2010_extent", "img_mng_chng_tile", "img_nmng_chng_tile", "img_mng_chng_lower_tile",
                "img_nmng_chng_lower_tile", "img_mng_chng_upper_tile", "img_nmng_chng_upper_tile", "calc_intervals", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])


if __name__ == "__main__":
    CreateTileStats().std_run()

