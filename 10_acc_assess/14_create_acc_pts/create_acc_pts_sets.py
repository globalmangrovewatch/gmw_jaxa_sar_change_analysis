import glob
import os

import rsgislib.vectorutils

input_acc_pts_files = glob.glob("acc_ref_pts/*.geojson")

set1_out_dir = "acc_ref_pts_set_1"
set2_out_dir = "acc_ref_pts_set_2"

for input_acc_pts_file in input_acc_pts_files:
    input_acc_pts_lyr = rsgislib.vectorutils.get_vec_lyrs_lst(input_acc_pts_file)[0]

    set1_out_vec_lyr = f"{input_acc_pts_lyr}_set1"
    set1_out_vec_file = os.path.join(set1_out_dir, f"{set1_out_vec_lyr}.geojson")

    set2_out_vec_lyr = f"{input_acc_pts_lyr}_set2"
    set2_out_vec_file = os.path.join(set2_out_dir, f"{set2_out_vec_lyr}.geojson")

    rsgislib.vectorutils.split_vec_lyr_random_subset(input_acc_pts_file, input_acc_pts_lyr, set1_out_vec_file, set1_out_vec_lyr, set2_out_vec_file, set2_out_vec_lyr, n_smpl=250, out_format='GeoJSON', rnd_seed=None)
