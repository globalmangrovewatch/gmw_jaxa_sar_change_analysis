import os
import h5py
import numpy
import matplotlib.pyplot as plt
import rsgislib
import pandas

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

def get_smp_counts_threshold(data, threshold):
    below_data = data[data < threshold]
    smps_below = below_data.shape[0]
    above_data = data[data > threshold]
    smps_above = above_data.shape[0]
    return smps_below, smps_above

def test_thresholds(in_h5_file, init_threshold, out_file, var_idx=1):
    rsgis_utils = rsgislib.RSGISPyUtils()
    init_threshold = init_threshold * 100
    print(init_threshold)
    # Get threshold for Mangrove Data
    fH5 = h5py.File(in_h5_file, 'r')
    data_shp = fH5['DATA/DATA'].shape
    print(data_shp)
    num_vars = data_shp[1]
    if var_idx >= num_vars:
        raise Exception("Var isn't within the dataset")
    data = numpy.array(fH5['DATA/DATA'])
    data = mask_data_to_valid(data, lower_limit=-5000, upper_limit=2000)
    data = data[..., var_idx]
    print(data.shape)

    thres_steps = numpy.arange(0, 1000, 50)
    thresholds = numpy.sort(numpy.concatenate(((init_threshold + thres_steps), (init_threshold - thres_steps[1:]))))

    out_stats = dict()
    for threshold in thresholds:
        smps_below, smps_above = get_smp_counts_threshold(data, threshold)
        out_stats[threshold] = dict()
        out_stats[threshold]['below'] = smps_below
        out_stats[threshold]['above'] = smps_above

    out_info = dict()
    out_info['threshold'] = init_threshold
    out_info['tests'] = out_stats

    rsgis_utils.writeDict2JSON(out_info, out_file)

def plot_result(in_stats_file, out_data_plot_file, out_percent_plot_file, out_xls_file, title_str, above=True):
    rsgis_utils = rsgislib.RSGISPyUtils()
    test_info = rsgis_utils.readJSON2Dict(in_stats_file)

    ref_above = float(test_info['tests'][str(test_info['threshold'])]['above'])
    ref_below = float(test_info['tests'][str(test_info['threshold'])]['below'])
    ref_total = ref_above+ref_below

    thresholds = list()
    smps_below = list()
    smps_above = list()
    smps_percent_below = list()
    smps_percent_above = list()

    for threshold in test_info['tests']:
        thresholds.append(float(threshold)/100)
        above_val = float(test_info['tests'][threshold]['above'])
        below_val = float(test_info['tests'][threshold]['below'])

        smps_above.append(above_val)
        smps_below.append(below_val)

        above_percent_diff = ((above_val-ref_above) / ref_total) * 100
        below_percent_diff = ((below_val-ref_below) / ref_total) * 100

        smps_percent_above.append(above_percent_diff)
        smps_percent_below.append(below_percent_diff)


    #print(smps_below)
    #print(thresholds)
    #print(test_info['threshold'])
    plt.figure()
    if above:
        plt.plot(thresholds, smps_above, label='above')
    else:
        plt.plot(thresholds, smps_below, label='below')
    plt.axvline(x=float(test_info['threshold'])/100, color='red')
    plt.title(title_str)
    plt.xlabel('Threshold')
    plt.ylabel('Pixel Count')
    plt.savefig(out_data_plot_file)

    plt.figure()
    if above:
        plt.plot(thresholds, smps_percent_above, label='above')
    else:
        plt.plot(thresholds, smps_percent_below, label='below')
    plt.axvline(x=float(test_info['threshold']) / 100, color='red')
    plt.title(title_str)
    plt.xlabel('Threshold')
    plt.ylabel('Percentage')
    plt.savefig(out_percent_plot_file)

    out_data_dict = dict()
    out_data_dict['thresholds'] = thresholds
    out_data_dict['above pxls'] = smps_above
    out_data_dict['below pxls'] = smps_below
    out_data_dict['above percent'] = smps_percent_above
    out_data_dict['below percent'] = smps_percent_below

    df = pandas.DataFrame.from_dict(out_data_dict)
    xls_writer = pandas.ExcelWriter(out_xls_file, engine='xlsxwriter')
    df.to_excel(xls_writer, sheet_name='threshold_sensitivity')
    xls_writer.save()


tile_dir = "/Users/pete/Temp/gmw_v3_analysis/single_scene_threshold_sensititivity_test/data/N06E005"

mng_data_2020 = os.path.join(tile_dir, "GMW_N06E005_2020_mng_dB.h5")
nmng_data_2020 = os.path.join(tile_dir, "GMW_N06E005_2020_not_mng_dB.h5")

years = [1996, 2007, 2008, 2009, 2015, 2016, 2017, 2018, 2019, 2020]
mng_hv_thresholds = [-19.19996048, -17.99259838, -18.00675027, -18.17585939, -19.41850488, -19.48240773, -19.39218967, -19.29984857, -19.19996048, -19.15597535]
nmng_hv_thresholds = [-23.9948732, -23.99543542, -23.9948732, -23.99554042, -23.68668732, -23.86523283, -23.69565974, -23.42131409, -23.99504198, -23.99499765]

mng_hh_thresholds = [-13.55576459, -13.07343154, -13.42548106, -13.37546399, -13.54758741, -13.72153459, -13.56394177, -13.88855784, -14.16830357, -14.4867319, -13.33981131, -13.55576459]
nmng_hh_thresholds = [-11.2900573, -11.6655056, -11.6655056, -11.6655056, -10.88533806, -11.19655213, -11.12787989, -10.22963897, -12.04095391, -12.2121533, -13.33981131, -13.55576459]

#test_thresholds(mng_data_2020, mng_hv_thresholds[9], "GMW_N06E005_2020_mng_thresholds.json")
#test_thresholds(nmng_data_2020, nmng_hv_thresholds[9], "GMW_N06E005_2020_nmng_thresholds.json")

plot_result("GMW_N06E005_2020_mng_thresholds.json", "GMW_N06E005_2020_mng_thresholds_plot.png", "GMW_N06E005_2020_mng_thresholds_percent_plot.png", "GMW_N06E005_2020_mng_thresholds_sum.xlsx", "Mangrove Change Thresholds (N06E005 2020)", above=True)
plot_result("GMW_N06E005_2020_nmng_thresholds.json", "GMW_N06E005_2020_nmng_thresholds_plot.png", "GMW_N06E005_2020_nmng_thresholds_percent_plot.png", "GMW_N06E005_2020_nmng_thresholds_sum.xlsx", "Not Mangrove Change Thresholds (N06E005 2020)", above=False)