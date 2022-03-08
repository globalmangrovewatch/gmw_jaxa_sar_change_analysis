import os
import glob

import rsgislib
import rsgislib.tools.filetools
import rsgislib.imageutils

def get_dir_name(input_file: str) -> str:
    """
    A function which returns just the name of the directory of the input path
    (file or directory) without the rest of the path.

    :param input_file: string for the input path (file or directory) name and path
    :return: directory name

    """
    input_file = os.path.abspath(input_file)
    if os.path.isfile(input_file):
        dir_path = os.path.dirname(input_file)
    elif os.path.isdir(input_file):
        dir_path = input_file
    else:
        raise rsgislib.RSGISPyException("Input path must be either a file or directory")
    dir_name = os.path.basename(dir_path)
    return dir_name

in_base_dir = "/Users/pete/Dropbox/University/Research/Analysis/GlobalMangroveWatch/gmw_v3_acc/landsat_raw"
out_base_dir = "/Users/pete/Dropbox/University/Research/Analysis/GlobalMangroveWatch/gmw_v3_acc/landsat_band_sub"

rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

in_dirs = rsgislib.tools.filetools.get_dir_list(in_base_dir)
for in_dir in in_dirs:
    in_dir_name = get_dir_name(in_dir)
    print(in_dir)
    print(in_dir_name)
    out_dir = os.path.join(out_base_dir, in_dir_name)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    imgs = glob.glob(os.path.join(in_dir, "*.tif"))
    for img in imgs:
        img_basename = rsgislib.tools.filetools.get_file_basename(img)
        out_img = os.path.join(out_dir, f"{img_basename}.tif")
        if not os.path.exists(out_img):
            if "1996" in img_basename:
                rsgislib.imageutils.select_img_bands(img, out_img, "GTIFF", rsgislib.TYPE_16UINT, [1,2,3,4,5,7])
            elif "2007" in img_basename:
                rsgislib.imageutils.select_img_bands(img, out_img, "GTIFF", rsgislib.TYPE_16UINT, [1,2,3,4,5,7])
            elif "2008" in img_basename:
                rsgislib.imageutils.select_img_bands(img, out_img, "GTIFF", rsgislib.TYPE_16UINT, [1,2,3,4,5,7])
            elif "2009" in img_basename:
                rsgislib.imageutils.select_img_bands(img, out_img, "GTIFF", rsgislib.TYPE_16UINT, [1,2,3,4,5,7])
            elif "2010" in img_basename:
                rsgislib.imageutils.select_img_bands(img, out_img, "GTIFF", rsgislib.TYPE_16UINT, [1,2,3,4,5,7])
            else:
                rsgislib.imageutils.select_img_bands(img, out_img, "GTIFF", rsgislib.TYPE_16UINT, [2,3,4,5,6,7])

            rsgislib.imageutils.set_band_names(out_img, band_names=["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"], feedback = False)
            rsgislib.imageutils.pop_img_stats(out_img, use_no_data=True, no_data_val=0, calc_pyramids=True)


