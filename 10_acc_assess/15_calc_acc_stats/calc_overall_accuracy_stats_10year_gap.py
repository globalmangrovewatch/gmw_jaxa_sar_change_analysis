import os
import glob
import random
import pprint

import geopandas
import numpy

import rsgislib.vectorutils
import rsgislib.classification.classaccuracymetrics
import rsgislib.tools.utils
import rsgislib.tools.filetools

set1_dir = "./acc_ref_pts_set_1"
set2_dir = "./acc_ref_pts_set_2"

acc_chng_pts_set_1_dir = "./acc_chng_pts_set_1"
acc_chng_pts_set_2_dir = "./acc_chng_pts_set_2"
acc_chng_pts_set_3_dir = "./acc_chng_pts_set_3"
acc_chng_pts_set_4_dir = "./acc_chng_pts_set_4"

set_1_files = glob.glob(os.path.join(set1_dir, "*.geojson"))
set_2_files = glob.glob(os.path.join(set2_dir, "*.geojson"))

set_acc_chng_1_files = glob.glob(os.path.join(acc_chng_pts_set_1_dir, "*.geojson"))
set_acc_chng_2_files = glob.glob(os.path.join(acc_chng_pts_set_2_dir, "*.geojson"))
set_acc_chng_3_files = glob.glob(os.path.join(acc_chng_pts_set_3_dir, "*.geojson"))
set_acc_chng_4_files = glob.glob(os.path.join(acc_chng_pts_set_4_dir, "*.geojson"))

acc_set_pt_files = set_1_files + set_2_files + set_acc_chng_1_files + set_acc_chng_2_files + set_acc_chng_3_files + set_acc_chng_4_files

acc_set_vld_files = list()
for acc_set_pt_file in acc_set_pt_files:
    basename = rsgislib.tools.filetools.get_file_basename(acc_set_pt_file)
    basename_comps = basename.split("_")
    #print(basename_comps)
    if basename_comps[0] == "site":
        base_year = basename_comps[2]
        chng_year = basename_comps[3]
    else:
        base_year = basename_comps[4]
        chng_year = basename_comps[5]
    #print(f"{base_year} -- {chng_year}")
    time_period = float(chng_year) - float(base_year)
    #print(time_period)
    if time_period >= 10:
        gpd_df = geopandas.read_file(acc_set_pt_file)
        processed_vals = gpd_df["Processed"].values
        n_vals = processed_vals.shape[0]
        if numpy.sum(processed_vals) == n_vals:
            acc_set_vld_files.append(acc_set_pt_file)
        gpd_df = None


gmw_all_acc_pts = "gmw_chng_ref_acc_pts_10year_gap.geojson"
rsgislib.vectorutils.merge_vector_files(
    vec_files = acc_set_vld_files,
    out_vec_file = gmw_all_acc_pts,
    out_vec_lyr = None,
    out_format = "GeoJSON",
    out_epsg = None,
)

n_pts = rsgislib.vectorutils.get_vec_feat_count(gmw_all_acc_pts)
print("Total Number of Points: {}".format(n_pts))


gmw_acc_stats_json = "gmw_chng_acc_stats_10year_gap.json"
gmw_acc_stats_csv = "gmw_chng_acc_stats_10year_gap.csv"
rsgislib.classification.classaccuracymetrics.calc_acc_ptonly_metrics_vecsamples(vec_file=gmw_all_acc_pts, vec_lyr="gmw_chng_ref_acc_pts_10year_gap", ref_col="chng_ref", cls_col="chng_cls", out_json_file=gmw_acc_stats_json, out_csv_file=gmw_acc_stats_csv)

gmw_acc_stats_conf_json = "gmw_chng_acc_stats_10year_gap_conf_int.json"
acc_vals = rsgislib.classification.classaccuracymetrics.calc_acc_ptonly_metrics_vecsamples_bootstrap_conf_interval(
    vec_file=gmw_all_acc_pts, vec_lyr="gmw_chng_ref_acc_pts_10year_gap", ref_col="chng_ref", cls_col="chng_cls",
    out_json_file=gmw_acc_stats_conf_json,
    sample_n_smps=3800,
    bootstrap_n=1000)
