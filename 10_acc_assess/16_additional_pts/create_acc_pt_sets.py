import glob
import os
import math

import rsgislib.vectorutils

input_acc_pts_files = glob.glob("acc_chng_pts/*.geojson")

set1_2_out_dir = "acc_chng_pts_set_1_2"
if not os.path.exists(set1_2_out_dir):
    os.mkdir(set1_2_out_dir)
set3_4_out_dir = "acc_chng_pts_set_3_4"
if not os.path.exists(set3_4_out_dir):
    os.mkdir(set3_4_out_dir)


set1_out_dir = "acc_chng_pts_set_1"
if not os.path.exists(set1_out_dir):
    os.mkdir(set1_out_dir)

set2_out_dir = "acc_chng_pts_set_2"
if not os.path.exists(set2_out_dir):
    os.mkdir(set2_out_dir)

set3_out_dir = "acc_chng_pts_set_3"
if not os.path.exists(set3_out_dir):
    os.mkdir(set3_out_dir)

set4_out_dir = "acc_chng_pts_set_4"
if not os.path.exists(set4_out_dir):
    os.mkdir(set4_out_dir)


for input_acc_pts_file in input_acc_pts_files:
    print(input_acc_pts_file)
    n_feats = rsgislib.vectorutils.get_vec_feat_count(input_acc_pts_file)
    n_set_feats = int(math.floor(n_feats/4))

    input_acc_pts_lyr = rsgislib.vectorutils.get_vec_lyrs_lst(input_acc_pts_file)[0]

    set1_2_out_vec_lyr = f"{input_acc_pts_lyr}_set1_2"
    set1_2_out_vec_file = os.path.join(set1_2_out_dir, f"{set1_2_out_vec_lyr}.geojson")

    set3_4_out_vec_lyr = f"{input_acc_pts_lyr}_set3_4"
    set3_4_out_vec_file = os.path.join(set3_4_out_dir, f"{set3_4_out_vec_lyr}.geojson")

    rsgislib.vectorutils.split_vec_lyr_random_subset(input_acc_pts_file, input_acc_pts_lyr, set1_2_out_vec_file, set1_2_out_vec_lyr, set3_4_out_vec_file, set3_4_out_vec_lyr, n_smpl=(n_set_feats*2), out_format='GeoJSON', rnd_seed=None)

    set1_out_vec_lyr = f"{input_acc_pts_lyr}_set1"
    set1_out_vec_file = os.path.join(set1_out_dir, f"{set1_out_vec_lyr}.geojson")

    set2_out_vec_lyr = f"{input_acc_pts_lyr}_set2"
    set2_out_vec_file = os.path.join(set2_out_dir, f"{set2_out_vec_lyr}.geojson")

    rsgislib.vectorutils.split_vec_lyr_random_subset(set1_2_out_vec_file, set1_2_out_vec_lyr, set1_out_vec_file, set1_out_vec_lyr, set2_out_vec_file, set2_out_vec_lyr, n_smpl=n_set_feats, out_format='GeoJSON', rnd_seed=None)

    set3_out_vec_lyr = f"{input_acc_pts_lyr}_set3"
    set3_out_vec_file = os.path.join(set3_out_dir, f"{set3_out_vec_lyr}.geojson")

    set4_out_vec_lyr = f"{input_acc_pts_lyr}_set4"
    set4_out_vec_file = os.path.join(set4_out_dir, f"{set4_out_vec_lyr}.geojson")

    rsgislib.vectorutils.split_vec_lyr_random_subset(set3_4_out_vec_file, set3_4_out_vec_lyr, set3_out_vec_file, set3_out_vec_lyr, set4_out_vec_file, set4_out_vec_lyr, n_smpl=n_set_feats, out_format='GeoJSON', rnd_seed=None)