import matplotlib.pyplot as plt
from matplotlib import colors
import pprint
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


def create_plot(gt_thresholds, pxls_gt, thresholds_lt, pxls_lt, title_str, op_threshold=None, out_file=None):
    plt.figure()
    plt.plot(gt_thresholds, pxls_gt, label='GMW')
    plt.plot(thresholds_lt, pxls_lt, label='PoChng')
    plt.legend()
    if op_threshold is not None:
        plt.axvline(x=op_threshold, color='red')
    plt.title(title_str)
    if out_file is not None:
        plt.savefig(out_file)
    else:
        plt.show()


def find_optimal_thresholds(input_file):
    print(input_file)
    data_dict = readJSON2Dict(input_file)
    pprint.pprint(data_dict)
    n_gmw_pxls = float(data_dict['gmw_pxls'])
    n_pochng_pxls = float(data_dict['pochng_pxls'])

    thresholds_gt = numpy.array(data_dict['thresholds_gt'])/100.0
    thresholds_lt = numpy.array(data_dict['thresholds_lt'])/100.0

    gmw_pxls_gt = numpy.array(data_dict['gmw_pxls_gt'])

    #gmw_pxls_gt = numpy.concatenate((gmw_pxls_gt[0], gmw_pxls_gt[1:]-gmw_pxls_gt[:-1]))


    pochng_pxls_gt = numpy.array(data_dict['pochng_pxls_gt'])

    gmw_pxls_lt = numpy.array(data_dict['gmw_pxls_lt'])
    pochng_pxls_lt = numpy.array(data_dict['pochng_pxls_lt'])



    gmw_pxls_gt_norm = gmw_pxls_gt / n_gmw_pxls
    pochng_pxls_gt_norm = pochng_pxls_gt / n_pochng_pxls

    gmw_pxls_lt_norm = gmw_pxls_lt / n_gmw_pxls
    pochng_pxls_lt_norm = pochng_pxls_lt / n_pochng_pxls

    #create_plot(thresholds_gt, gmw_pxls_gt_norm, thresholds_lt, pochng_pxls_lt_norm, "GMW than threshold", op_threshold=-23, out_file='gmw_chng_plot.png')

    #create_plot(thresholds_gt, pochng_pxls_gt_norm, thresholds_lt, gmw_pxls_lt_norm, "Potent Change than threshold", op_threshold=-23, out_file='pochng_plot.png')

    pochng_pxls_lt = numpy.concatenate(([pochng_pxls_lt[0]], pochng_pxls_lt[1:] - pochng_pxls_lt[:-1]))

    pochng_pxls_lt = pochng_pxls_lt / n_pochng_pxls

    n_steps = len(thresholds_gt)
    cu_sum = 0.0
    pochng_threshold = 0.0
    for i in range(n_steps):
        print("{}: {}".format(thresholds_lt[i], pochng_pxls_lt[i]))
        cu_sum += pochng_pxls_lt[i]
        print(cu_sum)
        if cu_sum > 0.99:
            pochng_threshold = thresholds_lt[i]
            break

    print("Potential Change threshold: {}".format(pochng_threshold))

    create_plot(thresholds_gt, pochng_pxls_gt_norm, thresholds_lt, gmw_pxls_lt_norm, "Potent Change than threshold", op_threshold=pochng_threshold, out_file='pochng_plot.png')







    gmw_pxls_lt = numpy.concatenate(([gmw_pxls_lt[0]], gmw_pxls_lt[1:] - gmw_pxls_lt[:-1]))

    gmw_pxls_lt = gmw_pxls_lt / n_gmw_pxls
    gmw_pxls_lt = numpy.flip(gmw_pxls_lt)
    thresholds_lt = numpy.flip(thresholds_lt)

    n_steps = len(thresholds_gt)
    cu_sum = 0.0
    gmw_threshold = 0.0
    for i in range(n_steps):
        print("{}: {}".format(thresholds_lt[i], gmw_pxls_lt[i]))
        cu_sum += gmw_pxls_lt[i]
        print(cu_sum)
        if cu_sum > 0.99:
            gmw_threshold = thresholds_lt[i]
            break

    print("GMW Change threshold: {}".format(gmw_threshold))

    create_plot(thresholds_gt, gmw_pxls_gt_norm, thresholds_lt, pochng_pxls_lt_norm, "GMW than threshold", op_threshold=gmw_threshold, out_file='gmw_chng_plot.png')




test_file = '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_test_thresholds/GMW_N14E122_2010_threshold_tests.json'
#test_file = '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_test_thresholds/GMW_S36E174_2010_threshold_tests.json'
#test_file = '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_test_thresholds/GMW_S14E141_2010_threshold_tests.json'
#test_file = '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_test_thresholds/GMW_S36E149_2010_threshold_tests.json'
find_optimal_thresholds(test_file)
