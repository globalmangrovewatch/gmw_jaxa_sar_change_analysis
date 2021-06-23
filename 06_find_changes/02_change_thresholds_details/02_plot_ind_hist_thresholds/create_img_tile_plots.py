from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imageutils
import h5py
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors

logger = logging.getLogger(__name__)

def mask_data_to_valid(data, lower_limit=None, upper_limit=None):
    data = data[numpy.isfinite(data).all(axis=1)]
    if lower_limit is not None:
        data = data[numpy.any(data > lower_limit, axis=1)]
    if upper_limit is not None:
        data = data[numpy.any(data < upper_limit, axis=1)]
    return data


def plot_histo(data, threshold, title_str, out_file):
    data = data[data > -5000]
    data = data[data < 2000]

    data = data / 100
    threshold = threshold / 100
    print(data.shape)
    print(data.min())
    print(data.max())

    plt.figure()
    plt.hist(data, bins=100)
    plt.axvline(x=threshold, color='red')
    plt.title(title_str)
    plt.savefig(out_file)


def plot_2dhisto(data, thresholds, title_str, out_file):
    data = data / 100
    thresholds[0] = thresholds[0] / 100
    thresholds[1] = thresholds[1] / 100
    print(data.shape)
    print(data.min())
    print(data.max())

    plt.figure()
    plt.hist2d(data[..., 0], data[..., 1], bins=100, norm=colors.LogNorm())
    plt.axvline(x=thresholds[0], color='red')
    plt.axhline(y=thresholds[1], color='red')
    plt.title(title_str)
    plt.savefig(out_file)


def plot_pair_histo(mng_data, nmng_data, mng_thres, nmng_thres, title_str, out_file):
    mng_data = mng_data[mng_data > -5000]
    mng_data = mng_data[mng_data < 2000]
    mng_data = mng_data / 100
    mng_thres = mng_thres / 100

    nmng_data = nmng_data[nmng_data > -5000]
    nmng_data = nmng_data[nmng_data < 2000]
    nmng_data = nmng_data / 100
    nmng_thres = nmng_thres / 100

    plt.figure()
    plt.hist(mng_data, bins=100, color='green')
    plt.hist(nmng_data, bins=100, color='blue')
    plt.axvline(x=mng_thres, color='red')
    plt.axvline(x=nmng_thres, color='yellow')
    plt.title(title_str)
    plt.savefig(out_file)


class CreateImageTilePlots(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile_plots.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()

        if os.path.exists():
            thres_vals = rsgis_utils.readJSON2Dict(self.params['thres_file'])
        else:
            thres_vals = dict()
            thres_vals['mng_hh'] = 0.0
            thres_vals['mng_hv'] = 0.0
            thres_vals['nmng_hh'] = 0.0
            thres_vals['nmng_hv'] = 0.0

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
            merged_nmng_data = self.params['nmng_data_files'][0]
        else:
            raise Exception("No non-mangrove data files!")

        # Get threshold for Mangrove Data
        fH5 = h5py.File(merged_mng_data, 'r')
        data_shp = fH5['DATA/DATA'].shape
        print(data_shp)
        num_mng_vars = data_shp[1]
        mng_data = numpy.array(fH5['DATA/DATA'])
        mng_data = mask_data_to_valid(mng_data, lower_limit=-5000, upper_limit=2000)

        fH5 = h5py.File(merged_nmng_data, 'r')
        data_shp = fH5['DATA/DATA'].shape
        num_nmng_vars = data_shp[1]
        nmng_data = numpy.array(fH5['DATA/DATA'])
        nmng_data = mask_data_to_valid(nmng_data, lower_limit=-5000, upper_limit=2000)

        if num_mng_vars != num_nmng_vars:
            raise Exception("Number of variables is not equal!")

        if num_mng_vars == 1:
            plot_histo(mng_data[..., 0], thres_vals['mng_hh'], '{} {} Mangrove HH'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_mangrove_hh.png'.format(self.params['gmw_prj'], self.params['year']))
            plot_histo(mng_data[..., 1], thres_vals['mng_hv'], '{} {} Mangrove HV'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_mangrove_hv.png'.format(self.params['gmw_prj'], self.params['year']))

            plot_histo(nmng_data[..., 0], thres_vals['nmng_hh'], '{} {} Not Mangrove HH'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_not_mangrove_hh.png'.format(self.params['gmw_prj'], self.params['year']))
            plot_histo(nmng_data[..., 1], thres_vals['nmng_hv'], '{} {} Not Mangrove HV'.format(self.params['gmw_prj'], self.params['year']),  '{}_{}_not_mangrove_hv.png'.format(self.params['gmw_prj'], self.params['year']))

            plot_pair_histo(mng_data[..., 0], nmng_data[..., 0], thres_vals['mng_hh'], thres_vals['nmng_hh'], '{} {} HH'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_hist_hh.png'.format(self.params['gmw_prj'], self.params['year']))
            plot_pair_histo(mng_data[..., 1], nmng_data[..., 1], thres_vals['mng_hv'], thres_vals['nmng_hv'], '{} {} HV'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_hist_hv.png'.format(self.params['gmw_prj'], self.params['year']))

            plot_2dhisto(mng_data, [thres_vals['mng_hh'], thres_vals['mng_hv']], '{} {} Mangroves'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_2dhist_mng.png'.format(self.params['gmw_prj'], self.params['year']))
            plot_2dhisto(nmng_data, [thres_vals['nmng_hh'], thres_vals['nmng_hv']], '{} {} Not Mangroves'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_2dhist_not_mng.png'.format(self.params['gmw_prj'], self.params['year']))
        elif num_mng_vars == 1: # JERS-1 only has HH
            plot_histo(mng_data[..., 0], thres_vals['mng_hh'], '{} {} Mangrove HH'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_mangrove_hh.png'.format(self.params['gmw_prj'], self.params['year']))
            plot_histo(nmng_data[..., 0], thres_vals['nmng_hh'], '{} {} Not Mangrove HH'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_not_mangrove_hh.png'.format(self.params['gmw_prj'], self.params['year']))
            plot_pair_histo(mng_data[..., 0], nmng_data[..., 0], thres_vals['mng_hh'], thres_vals['nmng_hh'], '{} {} HH'.format(self.params['gmw_prj'], self.params['year']), '{}_{}_hist_hh.png'.format(self.params['gmw_prj'], self.params['year']))

    def required_fields(self, **kwargs):
        return ["gmw_prj", "year", "mng_data_files", "nmng_data_files", "thres_file", "out_dir", "out_cmp_file", "tmp_dir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_cmp_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_cmp_file']):
            os.remove(self.params['out_cmp_file'])

        import glob
        prj_files = glob.glob(os.path.join(self.params['out_dir'], "{}_{}*.png".format(self.params['gmw_prj'], self.params['year'])))
        for prj_plt_file in prj_files:
            if os.path.exists(prj_plt_file):
                os.remove(prj_plt_file)

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTilePlots().std_run()


