import glob
import os
import numpy

import rsgislib.tools.filetools
import rsgislib.imagecalc
import rsgislib.rastergis


def add_non_mng_cls(input_img, output_img):
    basename = rsgislib.tools.filetools.get_file_basename(img)
    
    band_defns = list()
    band_defns.append(rsgislib.imagecalc.BandDefn('mng', input_img, 1))
    rsgislib.imagecalc.band_math(output_img, '(mng==1)?1:2', 'KEA', rsgislib.TYPE_8UINT, band_defns)
    
    rsgislib.rastergis.pop_rat_img_stats(output_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)
    unq_vals = rsgislib.imagecalc.get_unique_values(output_img)
    print(unq_vals)
    rsgislib.rastergis.set_column_data(output_img, "cls_name", numpy.array(["", "Mangrove", "Other"]))


out_dir = "../00_datasets/roi_v314_cls_imgs"
imgs = glob.glob("../00_datasets/roi_v314_imgs/*.kea")
for img in imgs:
    basename = rsgislib.tools.filetools.get_file_basename(img)
    out_img = os.path.join(out_dir, "{}_cls.kea".format(basename))
    add_non_mng_cls(img, out_img)



