import matplotlib.pyplot as plt
import numpy

def readJSON2Dict(input_file):
    """
    Read a JSON file. Will return a list or dict.

    :param input_file: input JSON file path.

    """
    import json
    with open(input_file) as f:
        data = json.load(f)
    return data

def writeDict2JSON(data_dict, out_file):
    """
    Write some data to a JSON file. The data would commonly be structured as a dict but could also be a list.

    :param data_dict: The dict (or list) to be written to the output JSON file.
    :param out_file: The file path to the output file.

    """
    import json
    with open(out_file, 'w') as fp:
        json.dump(data_dict, fp, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


def create_sngl_plot(thresholds, pxls_counts, title_str, data_lbl, op_threshold=None, out_file=None):
    plt.figure()
    plt.plot(thresholds, pxls_counts, label=data_lbl)
    plt.legend()
    if op_threshold is not None:
        plt.axvline(x=op_threshold, color='red')
    plt.title(title_str)
    if out_file is not None:
        plt.savefig(out_file)
    else:
        plt.show()

def create_dual_plot(gmw_thresholds, gmw_pxls_counts, pochng_thresholds, prochng_pxls_counts, title_str, op_gmw_threshold=None, op_pochng_threshold=None, out_file=None):
    plt.figure()
    plt.plot(gmw_thresholds, gmw_pxls_counts, label='Mangrove', color='green')
    plt.plot(pochng_thresholds, prochng_pxls_counts, label='Po-Chng', color='blue')
    plt.legend()
    if op_gmw_threshold is not None:
        plt.axvline(x=op_gmw_threshold, color='green')
    if op_pochng_threshold is not None:
        plt.axvline(x=op_pochng_threshold, color='blue')
    plt.title(title_str)
    if out_file is not None:
        plt.savefig(out_file)
    else:
        plt.show()


def find_signal_optimal_threshold(n_pxls, thresholds, thres_pxl_counts, data_lbl, prop_thres=0.95, reverse=False):

    if reverse:
        prop_thres = 1 - prop_thres

    bin_pxl_counts = numpy.concatenate(([thres_pxl_counts[0]], thres_pxl_counts[1:] - thres_pxl_counts[:-1]))

    thres_pxl_prop = bin_pxl_counts / n_pxls

    n_steps = len(thresholds)
    cu_sum = 0.0
    op_threshold = 0.0
    for i in range(n_steps):
        #print("{}: {}".format(thresholds[i], thres_pxl_prop[i]))
        cu_sum += thres_pxl_prop[i]
        #print("\t{}".format(cu_sum))
        if cu_sum > prop_thres:
            op_threshold = thresholds[i]
            break

    #create_sngl_plot(thresholds, thres_pxl_prop, "Test", data_lbl, op_threshold, out_file=None)

    return op_threshold



def run_find_optimal_thresholds(input_file, output_file=None, output_plot_file=None):
    data_dict = readJSON2Dict(input_file)
    n_gmw_pxls = float(data_dict['gmw_pxls'])
    n_pochng_pxls = float(data_dict['pochng_pxls'])

    thresholds_gt = numpy.array(data_dict['thresholds_gt'])/100.0
    thresholds_lt = numpy.array(data_dict['thresholds_lt'])/100.0

    gmw_pxls_gt = numpy.array(data_dict['gmw_pxls_gt'])
    pochng_pxls_gt = numpy.array(data_dict['pochng_pxls_gt'])

    gmw_pxls_lt = numpy.array(data_dict['gmw_pxls_lt'])
    pochng_pxls_lt = numpy.array(data_dict['pochng_pxls_lt'])
    if n_gmw_pxls > 0:
        op_gmw_threshold = find_signal_optimal_threshold(n_gmw_pxls, thresholds_lt, gmw_pxls_lt, 'GMW', reverse=True)
        print("Mangrove Threshold: {}".format(op_gmw_threshold))
    else:
        op_gmw_threshold = 0

    if n_pochng_pxls > 0:
        op_pochng_threshold = find_signal_optimal_threshold(n_pochng_pxls, thresholds_lt, pochng_pxls_lt, 'Po-Change', reverse=False)
        print("Potential Change Threshold: {}".format(op_pochng_threshold))
    else:
        op_pochng_threshold = 0

    if (n_gmw_pxls > 0) and (n_pochng_pxls > 0):
        create_dual_plot(thresholds_lt, gmw_pxls_lt/n_gmw_pxls, thresholds_lt, pochng_pxls_gt/n_pochng_pxls, "Compare GMW and Potential Change Values",
                     op_gmw_threshold=op_gmw_threshold, op_pochng_threshold=op_pochng_threshold, out_file=output_plot_file)
    elif n_gmw_pxls > 0:
        create_sngl_plot(thresholds_lt, gmw_pxls_lt/n_gmw_pxls, "Mangrove Threshold", 'Mangrove', op_gmw_threshold, out_file=output_plot_file)
    elif n_pochng_pxls > 0:
        create_sngl_plot(thresholds_lt, pochng_pxls_lt/n_pochng_pxls, "Potential Change Threshold", 'Potential Change', op_pochng_threshold, out_file=output_plot_file)

    if output_file is not None:
        out_thresholds = dict()
        out_thresholds['mangrove'] = op_gmw_threshold
        out_thresholds['not-mangrove'] = op_pochng_threshold

        writeDict2JSON(out_thresholds, output_file)


import glob
import os
"""
out_dir = '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_tile_thresholds'
tile_files = glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_test_thresholds/*.json')
for tile_file in tile_files:
    tile_name = os.path.splitext(os.path.basename(tile_file))[0].split('_')[1]
    #print("{}:\n\t{}".format(tile_file, tile_name))
    out_file = os.path.join(out_dir, "{}_thresholds.json".format(tile_name))
    out_plot_file = os.path.join(out_dir, "{}_thresholds.png".format(tile_name))
    run_find_optimal_thresholds(tile_file, out_file, out_plot_file)
"""

"""
# Global Stats
run_find_optimal_thresholds('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/global_stats.json', '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/global_thresholds.json', '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/global_thresholds_plots.png')
"""


out_dir = '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_prj_info_thresholds'
tile_files = glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_prj_info/*.json')
for tile_file in tile_files:
    tile_name = os.path.splitext(os.path.basename(tile_file))[0].split('_')[0]
    #print("{}:\n\t{}".format(tile_file, tile_name))
    out_file = os.path.join(out_dir, "{}_thresholds.json".format(tile_name))
    out_plot_file = os.path.join(out_dir, "{}_thresholds.png".format(tile_name))
    run_find_optimal_thresholds(tile_file, out_file, out_plot_file)
