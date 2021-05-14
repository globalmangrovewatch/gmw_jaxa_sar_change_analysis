from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imageutils
import h5py
import numpy
import scipy.optimize
import scipy.stats

logger = logging.getLogger(__name__)


def mask_data_to_valid(data, lower_limit=None, upper_limit=None):
    data = data[numpy.isfinite(data).all(axis=1)]
    if lower_limit is not None:
        data = data[numpy.any(data > lower_limit, axis=1)]
    if upper_limit is not None:
        data = data[numpy.any(data < upper_limit, axis=1)]
    return data


def calc_chng_threshold(data, max_val, min_val, init_thres, low_thres=True):
    if len(data.shape) > 1:
        raise Exception("Expecting a single variable.")
    print("Mean: {}".format(numpy.mean(data)))
    print("Std Dev: {}".format(numpy.std(data)))
    print("Min: {}".format(numpy.min(data)))
    print("Max: {}".format(numpy.max(data)))

    def _opt_fun(x, *args):
        data = args[0]
        if low_thres:
            # Subset by x threshold
            data_sub = data[data > x]
        else:
            # Subset by x threshold
            data_sub = data[data < x]

        # calculate kurtosis and skewness
        kurtosis = scipy.stats.kurtosis(data_sub)
        skew = scipy.stats.skew(data_sub)
        # Product of kurtosis and skewness
        kur_skew = abs(kurtosis + skew)

        return kur_skew

    opt_rslt = scipy.optimize.dual_annealing(_opt_fun, bounds=[(min_val, max_val)], args=[data], x0=[init_thres])

    #print(opt_rslt)

    out_thres = None
    if opt_rslt.success:
        out_thres = opt_rslt.x[0]
        print("Success in retrieving threshold... {}".format(out_thres))
    else:
        print(opt_rslt)

    return out_thres


class CalcProjectThreholds(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='calc_project_thresholds.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()

        # Create output data structure.
        out_thres_lut = dict()
        out_thres_lut['mng_hh'] = 0.0
        out_thres_lut['nmng_hh'] = 0.0

        # Merge mangrove data
        if len(self.params['mng_data_files']) > 1:
            merged_mng_data = os.path.join(self.params['tmp_dir'], "{}_merged_mng.h5".format(self.params['gmw_prj']))
            rsgislib.imageutils.mergeExtractedHDF5Data(self.params['mng_data_files'], merged_mng_data)
        elif len(self.params['mng_data_files']) == 1:
            merged_mng_data = self.params['mng_data_files'][0]
        else:
            raise Exception("No mangrove data files!")

        # merge non-mangrove data
        if len(self.params['nmng_data_files']) > 1:
            merged_nmng_data = os.path.join(self.params['tmp_dir'], "{}_merged_nmng.h5".format(self.params['gmw_prj']))
            rsgislib.imageutils.mergeExtractedHDF5Data(self.params['nmng_data_files'], merged_nmng_data)
        elif len(self.params['nmng_data_files']) == 1:
            merged_mng_data = self.params['nmng_data_files'][0]
        else:
            raise Exception("No non-mangrove data files!")

        # Get threshold for Mangrove Data
        fH5 = h5py.File(merged_mng_data, 'r')
        data_shp = fH5['DATA/DATA'].shape
        print(data_shp)
        num_vars = data_shp[1]
        mng_data = numpy.array(fH5['DATA/DATA'])
        print(mng_data.shape)
        print(mng_data)
        mng_data = mask_data_to_valid(mng_data, lower_limit=-5000, upper_limit=2000)
        print(mng_data.shape)
        out_thres_lut['mng_hh'] = float(calc_chng_threshold(mng_data[..., 0], max_val=-800, min_val=-1800, init_thres=-1200, low_thres=False))
        print("mng_hh: {}".format(out_thres_lut['mng_hh']))
        if num_vars == 2:
            out_thres_lut['mng_hv'] = 0.0
            out_thres_lut['mng_hv'] = float(calc_chng_threshold(mng_data[..., 1], max_val=-1200, min_val=-2400, init_thres=-1400, low_thres=False))
            print("mng_hv: {}".format(out_thres_lut['mng_hv']))
        mng_data = None
        fH5.close()

        # Get threshold for Non-Mangrove Data
        fH5 = h5py.File(merged_nmng_data, 'r')
        data_shp = fH5['DATA/DATA'].shape
        num_vars = data_shp[1]
        nmng_data = numpy.array(fH5['DATA/DATA'])
        nmng_data = mask_data_to_valid(nmng_data, lower_limit=-5000, upper_limit=2000)
        out_thres_lut['nmng_hh'] = float(calc_chng_threshold(nmng_data[..., 0], max_val=-800, min_val=-2000, init_thres=-1200, low_thres=True))
        print("nmng_hh: {}".format(out_thres_lut['nmng_hh']))
        if num_vars == 2:
            out_thres_lut['nmng_hv'] = 0.0
            out_thres_lut['nmng_hv'] = float(calc_chng_threshold(nmng_data[..., 1], max_val=-1400, min_val=-3000, init_thres=-2000, low_thres=True))
            print("nmng_hv: {}".format(out_thres_lut['nmng_hv']))
        nmng_data = None
        fH5.close()

        # Export output thresholds.
        rsgis_utils.writeDict2JSON(out_thres_lut, self.params['out_file'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["gmw_prj", "mng_data_files", "nmng_data_files", "out_file", "tmp_dir"]

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


