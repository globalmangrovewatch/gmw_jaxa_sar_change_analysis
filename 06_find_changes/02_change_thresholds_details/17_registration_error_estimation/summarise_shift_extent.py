import rsgislib
import numpy
import scipy.stats
import matplotlib.pyplot as plt
import pprint

def plot_histo(data, title_str, out_file=None):
    plt.figure()
    plt.hist(data, bins=10)
    plt.title(title_str)
    if out_file is not None:
        plt.savefig(out_file)
    else:
        plt.show()
        

def plot(data1, data2, title_str, out_file=None):
    plt.figure()
    plt.scatter(data1, data2)
    plt.title(title_str)
    if out_file is not None:
        plt.savefig(out_file)
    else:
        plt.show()





rsgis_utils = rsgislib.RSGISPyUtils()

shift_stats = rsgis_utils.readJSON2Dict("GMW_N06E005_2010_v3_shift_stats.json")

dists = list()
mng_exts = list()

for shift in shift_stats:
    dists.append(shift_stats[shift]["pxl_shift_dist"])
    mng_exts.append(shift_stats[shift]["mng_area"])



#plot_histo(mng_exts, "Mangrove Extents")
plot(dists, mng_exts, "Mangrove Extents", out_file=None)

mng_exts_arr = numpy.array(mng_exts)


stats_describe = scipy.stats.describe(mng_exts_arr)

pprint.pprint(stats_describe)





