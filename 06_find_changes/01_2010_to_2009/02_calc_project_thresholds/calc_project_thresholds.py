from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
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
        return ["tile", "gmw_tile", "potent_chng_msk_img", "sar_img", "out_mng_data", "out_nmng_data"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_mng_data']] = 'hdf5'
        files_dict[self.params['out_nmng_data']] = 'hdf5'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_mng_data']):
            os.remove(self.params['out_mng_data'])

        if os.path.exists(self.params['out_nmng_data']):
            os.remove(self.params['out_nmng_data'])

if __name__ == "__main__":
    CalcProjectThreholds().std_run()


