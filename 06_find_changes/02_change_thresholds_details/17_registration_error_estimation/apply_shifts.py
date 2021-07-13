import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.imageregistration
import numpy
import pprint
import math

def get_mng_pxl_counts(in_base_img, in_shifted_img):
    rsgis_utils = rsgislib.RSGISPyUtils()
    basename = rsgis_utils.get_file_basename(in_shifted_img)
    tmp_img = os.path.join('tmp', "{}_mng_chng.kea".format(basename))
    tmp_tif_img = os.path.join('tmp', "{}_mng_chng_tif.tif".format(basename))
    
    bandDefns = []
    bandDefns.append(rsgislib.imagecalc.BandDefn('base', in_base_img, 1))
    bandDefns.append(rsgislib.imagecalc.BandDefn('shift', in_shifted_img, 1))
    rsgislib.imagecalc.bandMath(tmp_img, '(base==1 && shift==1)?1:(base==1 && shift==0)?2:(base==0 && shift==1)?3:0', 'KEA', rsgislib.TYPE_8UINT, bandDefns)
    rsgislib.imageutils.gdal_translate(tmp_img, tmp_tif_img, gdal_format='GTIFF')
    
    return rsgislib.imagecalc.countPxlsOfVal(tmp_img, vals=[1,2,3])



base_img = "GMW_N06E005_2010_v3_mskd_edges.kea"

rsgis_utils = rsgislib.RSGISPyUtils()
basename = rsgis_utils.get_file_basename(base_img)

x_res = 0.000222222222222
y_res = 0.000222222222222

x_pxl_shifts = numpy.arange(-2, 3, 1)
y_pxl_shifts = numpy.arange(-2, 3, 1)

shift_sum_counts = dict()

for x_pxl_shift in x_pxl_shifts:
    x_shift = x_pxl_shift * x_res
    for y_pxl_shift in y_pxl_shifts:
        y_shift = y_pxl_shift * y_res
        
        shift_ref = "x{}_y{}".format(x_pxl_shift, y_pxl_shift)
        print("{}: {}, {}".format(shift_ref, x_shift, y_shift))

        out_flt_img = os.path.join('tmp', "{}_{}.kea".format(basename, shift_ref))
        rsgislib.imageregistration.applyOffset2Image(base_img, out_flt_img, 'KEA', rsgislib.TYPE_8UINT, x_shift, y_shift)
        
        out_flt_tif_img = os.path.join('tmp', "{}_{}.tif".format(basename, shift_ref))
        rsgislib.imageutils.gdal_translate(out_flt_img, out_flt_tif_img, gdal_format='GTIFF')
        
        shift_pxl_counts = get_mng_pxl_counts(base_img, out_flt_img)
        shift_sum_counts[shift_ref] = dict()
        shift_sum_counts[shift_ref]["x_pxl_shift"] = int(x_pxl_shift)
        shift_sum_counts[shift_ref]["y_pxl_shift"] = int(y_pxl_shift)
        shift_sum_counts[shift_ref]["pxl_shift_dist"] = float(math.sqrt((x_pxl_shift**2)+(y_pxl_shift**2)))
        shift_sum_counts[shift_ref]["x_shift"] = float(x_shift)
        shift_sum_counts[shift_ref]["y_shift"] = float(y_shift)
        shift_sum_counts[shift_ref]["shift_dist"] = float(math.sqrt((x_shift**2)+(y_shift**2)))
        shift_sum_counts[shift_ref]["mng_area"] = int(shift_pxl_counts[0])
        shift_sum_counts[shift_ref]["mng_gain"] = int(shift_pxl_counts[1])
        shift_sum_counts[shift_ref]["mng_loss"] = int(shift_pxl_counts[2])
        
        

pprint.pprint(shift_sum_counts)
rsgis_utils.writeDict2JSON(shift_sum_counts, "GMW_N06E005_2010_v3_shift_stats.json")


