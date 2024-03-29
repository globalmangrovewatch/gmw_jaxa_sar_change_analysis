from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imageutils
import numpy

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        rsgis_utils = rsgislib.RSGISPyUtils()
        n_bands = rsgis_utils.getImageBandCount(self.params['sar_tile'])

        out_stats = dict()
        out_stats['hh_sum'] = 0.0
        out_stats['hh_n'] = 0
        out_stats['hh_mean'] = 0.0
        out_stats['hh_stddev'] = 0.0
        out_stats['hv_sum'] = 0.0
        out_stats['hv_n'] = 0
        out_stats['hv_mean'] = 0.0
        out_stats['hv_stddev'] = 0.0

        if n_bands == 1:
            hh_vals = rsgislib.imageutils.extractImgPxlValsInMsk(self.params['sar_tile'], [1], self.params['sar_tile_msk'], 1, no_data=None)
            hh_vals = hh_vals[numpy.isfinite(hh_vals)]
            hh_vals = hh_vals[hh_vals > -5000]
            hh_vals = hh_vals[hh_vals < 2000]
            if hh_vals.flatten().shape[0] > 0:
                out_stats['hh_sum'] = int(numpy.sum(hh_vals))
                out_stats['hh_n'] = int(hh_vals.flatten().shape[0])
                out_stats['hh_mean'] = int(numpy.mean(hh_vals))
                out_stats['hh_stddev'] = int(numpy.std(hh_vals))
        else:
            hh_vals = rsgislib.imageutils.extractImgPxlValsInMsk(self.params['sar_tile'], [1], self.params['sar_tile_msk'], 1, no_data=None)
            hh_vals = hh_vals[numpy.isfinite(hh_vals)]
            hh_vals = hh_vals[hh_vals > -5000]
            hh_vals = hh_vals[hh_vals < 2000]
            if hh_vals.flatten().shape[0] > 0:
                out_stats['hh_sum'] = int(numpy.sum(hh_vals))
                out_stats['hh_n'] = int(hh_vals.flatten().shape[0])
                out_stats['hh_mean'] = int(numpy.mean(hh_vals))
                out_stats['hh_stddev'] = int(numpy.std(hh_vals))

            hv_vals = rsgislib.imageutils.extractImgPxlValsInMsk(self.params['sar_tile'], [2], self.params['sar_tile_msk'], 1, no_data=None)
            hv_vals = hv_vals[numpy.isfinite(hv_vals)]
            hv_vals = hv_vals[hv_vals > -5000]
            hv_vals = hv_vals[hv_vals < 2000]
            if hv_vals.flatten().shape[0] > 0:
                out_stats['hv_sum'] = int(numpy.sum(hv_vals))
                out_stats['hv_n'] = int(hv_vals.flatten().shape[0])
                out_stats['hv_mean'] = int(numpy.mean(hv_vals))
                out_stats['hv_stddev'] = int(numpy.std(hv_vals))

        rsgis_utils.writeDict2JSON(out_stats, self.params['out_file'])


    def required_fields(self, **kwargs):
        return ["sar_tile", "sar_tile_msk", "out_file"]


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


