import os
import glob
import rsgislib.tools.filetools
import rsgislib.classification

versions = ["313", "314", "315"]



acc_ref_pt_files = glob.glob("acc_ref_pts/*.geojson")
acc_chng_pt_files = glob.glob("acc_chng_pts/*.geojson")

# Don't forget to also populate with v312 - double check the error that lammert found.
chng_imgs_path = "../00_data/02_site_chng_maps"
for acc_pt_file in acc_ref_pt_files:
    basename = rsgislib.tools.filetools.get_file_basename(acc_pt_file)
    basename_comps = basename.split('_')
    site = basename_comps[3]
    base_year = basename_comps[4]
    chng_year = basename_comps[5]

    print(f"{basename} = ({site}): {base_year} -- {chng_year}")
    chng_img = os.path.join(chng_imgs_path, f"site_{site}", f"gmw_chng_site_{site}_{base_year}_{chng_year}.kea")
    if not os.path.exists(chng_img):
        raise Exception("Change Image does not exist: {}".format(chng_img))



for acc_pt_file in acc_chng_pt_files:
    basename = rsgislib.tools.filetools.get_file_basename(acc_pt_file)
    basename_comps = basename.split('_')
    site = basename_comps[1]
    base_year = basename_comps[2]
    chng_year = basename_comps[3]

    print(f"{basename} = ({site}):  {base_year} -- {chng_year}")
    chng_img = os.path.join(chng_imgs_path, f"site_{site}", f"gmw_chng_site_{site}_{base_year}_{chng_year}.kea")
    if not os.path.exists(chng_img):
        raise Exception("Change Image does not exist: {}".format(chng_img))


#

#rsgislib.classification.pop_class_info_accuracy_pts(input_img: str, vec_file: str, vec_lyr: str, rat_class_col: str, vec_class_col: str)