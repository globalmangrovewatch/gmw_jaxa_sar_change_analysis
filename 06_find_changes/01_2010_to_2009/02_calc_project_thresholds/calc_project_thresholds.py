from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imageutils

logger = logging.getLogger(__name__)

class CalcProjectThreholds(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='calc_project_thresholds.py', descript=None)

    def do_processing(self, **kwargs):

        

        if self.params['sar_img'] is not None:
            rsgis_utils = rsgislib.RSGISPyUtils()
            n_bands = rsgis_utils.getImageBandCount(self.params['sar_img'])
            if n_bands == 1:
                fileInfo = [rsgislib.imageutils.ImageBandInfo(self.params['sar_img'], 'sar', [1])]
            else:
                fileInfo = [rsgislib.imageutils.ImageBandInfo(self.params['sar_img'], 'sar', [1, 2])]

            rsgislib.imageutils.extractZoneImageBandValues2HDF(fileInfo, self.params['gmw_tile'], self.params['out_mng_data'], 1.0)
            rsgislib.imageutils.extractZoneImageBandValues2HDF(fileInfo, self.params['potent_chng_msk_img'], self.params['out_nmng_data'], 1.0)


    def required_fields(self, **kwargs):
        return ["gmw_prj", "mng_data_files", "nmng_data_file", "out_file", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

            # Reset the tmp dir
            if os.path.exists(self.params['tmp_dir']):
                shutil.rmtree(self.params['tmp_dir'])
            os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CalcProjectThreholds().std_run()


