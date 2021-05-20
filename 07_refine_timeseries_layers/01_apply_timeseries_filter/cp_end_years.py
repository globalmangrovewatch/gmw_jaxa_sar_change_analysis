import glob
import shutil
import os
import rsgislib

def copy_imgs(imgs, out_dir, year):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    rsgis_utils = rsgislib.RSGISPyUtils()
    for img in imgs:
        basename = rsgis_utils.get_file_basename(img, n_comps=2)
        out_img = os.path.join(out_dir, "{}_{}_v3.kea".format(basename, year))
        shutil.copy(img, out_img)


imgs = glob.glob('/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_1996_v3/*v3_init.kea')
copy_imgs(imgs, '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_1996_v3_fnl', '1996')

imgs = glob.glob('/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2020_v3/*v3_init.kea')
copy_imgs(imgs, '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2020_v3_fnl', '2020')
