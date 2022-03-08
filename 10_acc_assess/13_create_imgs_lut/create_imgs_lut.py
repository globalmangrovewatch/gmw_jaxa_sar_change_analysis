import os
import glob
import pprint

import rsgislib
import rsgislib.tools.filetools
import rsgislib.tools.utils


base_dir = "/Users/pete/Dropbox/University/Research/Analysis/GlobalMangroveWatch/gmw_v3_acc/landsat_band_sub"

out_lut = dict()

in_dirs = rsgislib.tools.filetools.get_dir_list(base_dir)
for in_dir in in_dirs:

    imgs = glob.glob(os.path.join(in_dir, "*.tif"))
    for img in imgs:
        img_basename_comps = rsgislib.tools.filetools.get_file_basename(img).split("_")
        #print(img_basename_comps)
        site = int(img_basename_comps[1])
        if site not in out_lut:
            out_lut[site] = list()
        out_lut[site].append(int(img_basename_comps[5]))

rsgislib.tools.utils.write_dict_to_json(out_lut, "ls_imgs_lut.json")
