import os
import glob
import shutil

import numpy
import geopandas

set1_dir = "../15_calc_acc_stats/acc_ref_pts_set_1"
set2_dir = "../15_calc_acc_stats/acc_ref_pts_set_2"

acc_chng_pts_set_1_dir = "../15_calc_acc_stats/acc_chng_pts_set_1"
acc_chng_pts_set_2_dir = "../15_calc_acc_stats/acc_chng_pts_set_2"
acc_chng_pts_set_3_dir = "../15_calc_acc_stats/acc_chng_pts_set_3"
acc_chng_pts_set_4_dir = "../15_calc_acc_stats/acc_chng_pts_set_4"

set_1_files = glob.glob(os.path.join(set1_dir, "*.geojson"))
set_2_files = glob.glob(os.path.join(set2_dir, "*.geojson"))

acc_set_pt_files = set_1_files + set_2_files

set_acc_chng_1_files = glob.glob(os.path.join(acc_chng_pts_set_1_dir, "*.geojson"))
set_acc_chng_2_files = glob.glob(os.path.join(acc_chng_pts_set_2_dir, "*.geojson"))
set_acc_chng_3_files = glob.glob(os.path.join(acc_chng_pts_set_3_dir, "*.geojson"))
set_acc_chng_4_files = glob.glob(os.path.join(acc_chng_pts_set_4_dir, "*.geojson"))

acc_chng_set_pt_files = set_acc_chng_1_files + set_acc_chng_2_files + set_acc_chng_3_files + set_acc_chng_4_files

acc_set_vld_files = list()
for acc_set_pt_file in acc_set_pt_files:
    gpd_df = geopandas.read_file(acc_set_pt_file)
    processed_vals = gpd_df["Processed"].values
    n_vals = processed_vals.shape[0]
    if numpy.sum(processed_vals) == n_vals:
        acc_set_vld_files.append(acc_set_pt_file)
    gpd_df = None

acc_chng_set_vld_files = list()
for acc_set_pt_file in acc_chng_set_pt_files:
    gpd_df = geopandas.read_file(acc_set_pt_file)
    processed_vals = gpd_df["Processed"].values
    n_vals = processed_vals.shape[0]
    if numpy.sum(processed_vals) == n_vals:
        acc_chng_set_vld_files.append(acc_set_pt_file)
    gpd_df = None

out_dir = "acc_ref_pts"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for vld_file in acc_set_vld_files:
    shutil.copy2(vld_file, out_dir)

out_dir = "acc_chng_pts"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for vld_file in acc_chng_set_vld_files:
    shutil.copy2(vld_file, out_dir)
