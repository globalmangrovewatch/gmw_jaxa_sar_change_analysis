from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pprint
import shutil
import rsgislib
import rsgislib.imageutils
import h5py
import numpy
import scipy.optimize
import scipy.stats

logger = logging.getLogger(__name__)


def mask_data_to_valid(data, lower_limit=None, upper_limit=None):
    data = data[numpy.isfinite(data)]
    if lower_limit is not None:
        data = data[data > lower_limit]
    if upper_limit is not None:
        data = data[data < upper_limit]
    return data


def get_nbins_histogram(data):
    """
    Calculating the number of bins and the width of those bins for a histogram.

    :param data: 1-d numpy array.
    :return: (n_bins, bin_width) n_bins: int for the number of bins. bin_width: float with the width of the bins.

    """
    import numpy
    n = data.shape[0]
    lq = numpy.percentile(data, 25)
    uq = numpy.percentile(data, 75)
    iqr = uq - lq
    bin_width = 2 * iqr * n ** (-1 / 3)
    n_bins = int((numpy.max(data) - numpy.min(data)) / bin_width) + 2
    return n_bins, float(bin_width)


def get_bin_centres(bin_edges, geometric=False):
    """
    A function to calculate the centre points of bins from the bin edges from a histogram
    e.g., numpy.histogram. My default the arithmetic mean is provided (max+min)/2 but the
    geometric mean can also be calculated sqrt(min*max), this is useful for logarithmically
    spaced bins.

    :param bin_edges: numpy array of the bin edges
    :param geometric: boolean, if False (default) then the arithmetic mean return if True
                      then the geometric mean is returned.
    :returns: bin_centres - numpy array

    """
    import numpy
    if geometric:
        bin_centres = numpy.sqrt(bin_edges[1:] * bin_edges[:-1])
    else:
        bin_centres = (bin_edges[1:] + bin_edges[:-1]) / 2
    return bin_centres

def plot_histo(data, threshold, title_str, out_file=None):
    import matplotlib.pyplot as plt

    n_bins, bin_width = get_nbins_histogram(data)

    data = data / 100
    threshold = threshold / 100

    plt.figure()
    plt.hist(data, bins=n_bins)
    plt.axvline(x=threshold, color='red')
    plt.title(title_str)
    if out_file is None:
        plt.show()
    else:
        plt.savefig(out_file)

def calc_kurt_skew_threshold(data, max_val, min_val, init_thres, low_thres=True, contamination=10.0, only_kurtosis=False):
    import scipy.optimize
    import scipy.stats
    import numpy
    if len(data.shape) > 1:
        raise Exception("Expecting a single variable.")

    if (contamination < 1) or (contamination > 100):
        raise Exception("contamination parameter should have a value between 1 and 100.")

    if low_thres:
        low_percent = numpy.percentile(data, contamination)
        if low_percent < max_val:
            max_val = low_percent
    else:
        up_percent = numpy.percentile(data, 100 - contamination)
        if up_percent > min_val:
            min_val = up_percent

    if min_val == max_val:
        print("Min: {}".format(min_val))
        print("Max: {}".format(max_val))
        raise Exception("Min and Max values are the same.")
    elif min_val > max_val:
        print("Min: {}".format(min_val))
        print("Max: {}".format(max_val))
        raise Exception("Min value is greater than max - note this can happened if the "
                        "contamination parameter caused threshold to be changed.")

    if (init_thres < min_val) or (init_thres > max_val):
        print("Min: {}".format(min_val))
        print("Max: {}".format(max_val))
        print("Initial: {}".format(init_thres))
        raise Exception("The initial thresholds should be between the min/max values.")

    def _opt_fun(x, *args):
        data = args[0]
        if low_thres:
            # Subset by x threshold
            data_sub = data[data > x]
        else:
            # Subset by x threshold
            data_sub = data[data < x]

        # Calculate kurtosis and skewness
        kurtosis = scipy.stats.kurtosis(data_sub)
        if only_kurtosis:
            kur_skew = kurtosis
        else:
            skew = scipy.stats.skew(data_sub)
            # Product of kurtosis and skewness
            kur_skew = abs(kurtosis) + abs(skew)

        return kur_skew

    opt_rslt = scipy.optimize.dual_annealing(_opt_fun, bounds=[(min_val, max_val)], args=[data], x0=[init_thres])

    out_thres = None
    if opt_rslt.success:
        out_thres = opt_rslt.x[0]
    else:
        raise Exception("Optimisation failed, no threshold found.")

    return out_thres


def calc_yen_threshold(data):
    """
    A function to calculate yen threshold for a dataset. Input is expected
    to be a 1d numpy array.

    Yen J.C., Chang F.J., and Chang S. (1995) "A New Criterion
    for Automatic Multilevel Thresholding" IEEE Trans. on Image
    Processing, 4(3): 370-378. :DOI:`10.1109/83.366472`

    :param data: 1d numeric numpy array
    :returns: float (threshold)

    """
    import numpy
    # Note, this is based on the implementation within scikit-image

    # Calculate the histogram
    n_bins, bin_width = get_nbins_histogram(data)
    hist, bin_edges = numpy.histogram(data, bins=n_bins)
    bin_centres = get_bin_centres(bin_edges)

    # Normalization so we have probabilities-like values (sum=1)
    hist = hist.astype(numpy.float32)
    hist = 1.0 * hist / numpy.sum(hist)

    # Calculate probability mass function
    pmf = hist.astype(numpy.float32) / hist.sum()
    p1 = numpy.cumsum(pmf)  # Cumulative normalized histogram
    p1_sq = numpy.cumsum(pmf ** 2)
    # Get cumsum calculated from end of squared array:
    p2_sq = numpy.cumsum(pmf[::-1] ** 2)[::-1]
    # P2_sq indexes is shifted +1. I assume, with P1[:-1] it's help avoid
    # '-inf' in crit. ImageJ Yen implementation replaces those values by zero.
    crit = numpy.log(((p1_sq[:-1] * p2_sq[1:]) ** -1) * (p1[:-1] * (1.0 - p1[:-1])) ** 2)
    return bin_centres[crit.argmax()]

def getMergeExtractedHDF5Data(h5Files, variable=0):
    """
A function to get the data for a specific variable from a list of HDF files
 (e.g., from rsgislib.imageutils.extractZoneImageBandValues2HDF)

:param h5Files: a list of input files.
:param variable: the index for the variable of interest
:return: numpy array with the data or None is there is no data to return.

"""
    import h5py
    import numpy

    if variable < 0:
        raise Exception("The variable index must be greater than 0.")

    numVals = 0
    for h5File in h5Files:
        fH5 = h5py.File(h5File, 'r')
        dataShp = fH5['DATA/DATA'].shape
        if variable < dataShp[1]:
            numVals += dataShp[0]
        fH5.close()

    if numVals == 0:
        return None

    data_arr = numpy.zeros(numVals, dtype=float)

    rowInit = 0
    for h5File in h5Files:
        fH5 = h5py.File(h5File, 'r')
        dataShp = fH5['DATA/DATA'].shape
        if variable < dataShp[1]:
            numRows = fH5['DATA/DATA'].shape[0]
            data_arr[rowInit:(rowInit + numRows)] = fH5['DATA/DATA'][...,variable]
            rowInit += numRows
        fH5.close()

    return data_arr


class CalcProjectThreholds(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='calc_project_thresholds.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()

        # Create output data structure.
        out_thres_lut = dict()
        out_thres_lut['mng_hh_n'] = 0
        out_thres_lut['nmng_hh_n'] = 0
        out_thres_lut['mng_hv_n'] = 0
        out_thres_lut['nmng_hv_n'] = 0

        out_thres_lut['his_mng_hh'] = 0.0
        out_thres_lut['his_nmng_hh'] = 0.0
        out_thres_lut['his_mng_hv'] = 0.0
        out_thres_lut['his_nmng_hv'] = 0.0

        out_thres_lut['yen_mng_hh'] = 0.0
        out_thres_lut['yen_nmng_hh'] = 0.0
        out_thres_lut['yen_mng_hv'] = 0.0
        out_thres_lut['yen_nmng_hv'] = 0.0

        data = getMergeExtractedHDF5Data(self.params['mng_data_files'], variable=0)
        data = mask_data_to_valid(data, lower_limit=-5000, upper_limit=1000)
        plot_file = os.path.join(os.path.dirname(self.params['out_file']), '{}_hh_mng.png'.format(self.get_file_basename(self.params['out_file'])))
        plot_histo(data, -1400, 'Mangrove HH', out_file=plot_file)
        out_thres_lut['mng_hh_n'] = data.shape[0]
        out_thres_lut['his_mng_hh'] = float(calc_kurt_skew_threshold(data, max_val=-1000, min_val=-2000, init_thres=-1400, low_thres=True, contamination=10.0))
        out_thres_lut['yen_mng_hh'] = float(calc_yen_threshold(data))
        data = None

        data = getMergeExtractedHDF5Data(self.params['nmng_data_files'], variable=0)
        data = mask_data_to_valid(data, lower_limit=-5000, upper_limit=1000)
        plot_file = os.path.join(os.path.dirname(self.params['out_file']), '{}_hh_nmng.png'.format(self.get_file_basename(self.params['out_file'])))
        plot_histo(data, -1400, 'Not Mangrove HH', out_file=plot_file)
        out_thres_lut['nmng_hh_n'] = data.shape[0]
        out_thres_lut['his_nmng_hh'] = float(calc_kurt_skew_threshold(data, max_val=-1000, min_val=-2000, init_thres=-1400, low_thres=False, contamination=10.0))
        out_thres_lut['yen_nmng_hh'] = float(calc_yen_threshold(data))
        data = None

        data = getMergeExtractedHDF5Data(self.params['mng_data_files'], variable=1)
        data = mask_data_to_valid(data, lower_limit=-5000, upper_limit=1000)
        plot_file = os.path.join(os.path.dirname(self.params['out_file']), '{}_hv_mng.png'.format(self.get_file_basename(self.params['out_file'])))
        plot_histo(data, -1400, 'Mangrove HV', out_file=plot_file)
        out_thres_lut['mng_hv_n'] = data.shape[0]
        out_thres_lut['his_mng_hv'] = float(calc_kurt_skew_threshold(data, max_val=-1200, min_val=-2200, init_thres=-1600, low_thres=True, contamination=10.0))
        out_thres_lut['yen_mng_hv'] = float(calc_yen_threshold(data))
        data = None

        data = getMergeExtractedHDF5Data(self.params['nmng_data_files'], variable=1)
        data = mask_data_to_valid(data, lower_limit=-5000, upper_limit=1000)
        plot_file = os.path.join(os.path.dirname(self.params['out_file']), '{}_hv_nmng.png'.format(self.get_file_basename(self.params['out_file'])))
        plot_histo(data, -1400, 'Not Mangrove HV', out_file=plot_file)
        out_thres_lut['nmng_hv_n'] = data.shape[0]
        out_thres_lut['his_nmng_hv'] = float(calc_kurt_skew_threshold(data, max_val=-1200, min_val=-2200, init_thres=-1600, low_thres=False, contamination=10.0))
        out_thres_lut['yen_nmng_hv'] = float(calc_yen_threshold(data))
        data = None

        pprint.pprint(out_thres_lut)

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

