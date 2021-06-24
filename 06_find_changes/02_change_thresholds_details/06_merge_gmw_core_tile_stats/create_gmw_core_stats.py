from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imageutils
import h5py
import numpy
import pathlib

logger = logging.getLogger(__name__)

def mask_data_to_valid(data, lower_limit=None, upper_limit=None):
    data = data[numpy.isfinite(data).all(axis=1)]
    if lower_limit is not None:
        data = data[numpy.any(data > lower_limit, axis=1)]
    if upper_limit is not None:
        data = data[numpy.any(data < upper_limit, axis=1)]
    return data

def calc_stats(h5_file, out_stats_file):
    out_stats = dict()
    out_stats['hh_sum'] = 0.0
    out_stats['hh_n'] = 0
    out_stats['hh_mean'] = 0.0
    out_stats['hh_stddev'] = 0.0
    out_stats['hv_sum'] = 0.0
    out_stats['hv_n'] = 0
    out_stats['hv_mean'] = 0.0
    out_stats['hv_stddev'] = 0.0

    fH5 = h5py.File(h5_file, 'r')
    data_shp = fH5['DATA/DATA'].shape
    print(data_shp)
    num_feats = data_shp[0]
    if num_feats > 0:
        num_mng_vars = data_shp[1]
        mng_data = numpy.array(fH5['DATA/DATA'])
        mng_data = mask_data_to_valid(mng_data, lower_limit=-5000, upper_limit=2000)
        num_feats = data_shp[0]
        if num_feats > 0:
            if num_mng_vars > 1:
                out_stats['hh_sum'] = int(numpy.sum(mng_data[..., 0]))
                out_stats['hh_n'] = int(mng_data[..., 0].flatten().shape[0])
                out_stats['hh_mean'] = int(numpy.mean(mng_data[..., 0]))
                out_stats['hh_stddev'] = int(numpy.std(mng_data[..., 0]))

                out_stats['hv_sum'] = int(numpy.sum(mng_data[..., 1]))
                out_stats['hv_n'] = int(mng_data[..., 1].flatten().shape[0])
                out_stats['hv_mean'] = int(numpy.mean(mng_data[..., 1]))
                out_stats['hv_stddev'] = int(numpy.std(mng_data[..., 1]))
            elif num_mng_vars == 1:  # JERS-1 only has HH
                out_stats['hh_sum'] = int(numpy.sum(mng_data[..., 0]))
                out_stats['hh_n'] = int(mng_data[..., 0].flatten().shape[0])
                out_stats['hh_mean'] = int(numpy.mean(mng_data[..., 0]))
                out_stats['hh_stddev'] = int(numpy.std(mng_data[..., 0]))

            rsgis_utils = rsgislib.RSGISPyUtils()
            rsgis_utils.writeDict2JSON(out_stats, out_stats_file)
    fH5.close()

class CreateGMWCoreStats(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_gmw_core_stats.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        # Merge mangrove data
        if len(self.params['mng_data_files']) > 1:
            merged_mng_data = os.path.join(self.params['tmp_dir'], "{}_merged_mng.h5".format(self.params['gmw_prj']))
            rsgislib.imageutils.mergeExtractedHDF5Data(self.params['mng_data_files'], merged_mng_data)
        elif len(self.params['mng_data_files']) == 1:
            merged_mng_data = self.params['mng_data_files'][0]
        else:
            raise Exception("No mangrove data files!")

        calc_stats(merged_mng_data, self.params['out_prj_stats'])

        for mng_data_file in self.params['mng_data_files']:
            print("Processing Tile: {}".format(mng_data_file))
            basename = self.get_file_basename(mng_data_file)
            mng_stats_file = os.path.join(self.params['out_tile_dir'], '{}_stats.json'.format(basename))
            calc_stats(mng_data_file, mng_stats_file)

        pathlib.Path(self.params['out_cmp_file']).touch()

    def required_fields(self, **kwargs):
        return ["gmw_prj", "year", "mng_data_files", "out_tile_dir", "out_prj_stats", "out_cmp_file", "tmp_dir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_prj_stats']] = 'file'
        files_dict[self.params['out_cmp_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_cmp_file']):
            os.remove(self.params['out_cmp_file'])

        for mng_data_file in self.params['mng_data_files']:
            basename = self.get_file_basename(mng_data_file)
            mng_stats_file = os.path.join(self.params['out_tile_dir'], '{}_stats.json'.format(basename))
            if os.path.exists(mng_stats_file):
                os.remove(mng_stats_file)

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateGMWCoreStats().std_run()


