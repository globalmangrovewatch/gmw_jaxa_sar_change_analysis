import os
import glob
import pprint

import geopandas
import numpy

import rsgislib.vectorutils
import rsgislib.classification.classaccuracymetrics
import rsgislib.tools.utils

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
    gpd_df = geopandas.read_file(acc_set_pt_file)
    processed_vals = gpd_df["Processed"].values
    n_vals = processed_vals.shape[0]
    if numpy.sum(processed_vals) == n_vals:
        acc_set_vld_files.append(acc_set_pt_file)
    gpd_df = None

#print(len(acc_set_vld_files))

gmw_all_acc_pts = "gmw_chng_ref_acc_pts.geojson"
rsgislib.vectorutils.merge_vector_files(
    vec_files = acc_set_vld_files,
    out_vec_file = gmw_all_acc_pts,
    out_vec_lyr = None,
    out_format = "GeoJSON",
    out_epsg = None,
)

gmw_acc_stats_json = "gmw_chng_acc_stats.json"
gmw_acc_stats_csv = "gmw_chng_acc_stats.csv"
rsgislib.classification.classaccuracymetrics.calc_acc_ptonly_metrics_vecsamples(vec_file=gmw_all_acc_pts, vec_lyr="gmw_chng_ref_acc_pts", ref_col="chng_ref", cls_col="chng_cls", out_json_file=gmw_acc_stats_json, out_csv_file=gmw_acc_stats_csv)

tmp_dir = "tmp"
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

out_dir = "out_acc_stats"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)



acc_culm_pts_lst = list()
culm_n_pts = 0
culm_n_pts_lst = list()
acc_stats_dict = dict()
acc_stats_dict["Mangroves"] = list()
acc_stats_dict["Mangroves > Not Mangroves"] = list()
acc_stats_dict["Not Mangroves"] = list()
acc_stats_dict["Not Mangroves > Mangroves"] = list()
acc_stats_dict["Overall"] = list()

for acc_pts_file in acc_set_vld_files:
    print(acc_pts_file)
    c_n_pts = rsgislib.vectorutils.get_vec_feat_count(acc_pts_file, vec_lyr = None, compute_count = True)
    culm_n_pts += c_n_pts
    acc_culm_pts_lst.append(acc_pts_file)
    c_pts_vec_file = os.path.join(tmp_dir, "acc_pts_{}.geojson".format(culm_n_pts))
    c_pts_vec_lyr = "acc_pts_{}".format(culm_n_pts)
    rsgislib.vectorutils.merge_vector_files(
        vec_files=acc_culm_pts_lst,
        out_vec_file=c_pts_vec_file,
        out_vec_lyr=c_pts_vec_lyr,
        out_format="GeoJSON",
        out_epsg=None,
        )

    gmw_acc_stats_json = os.path.join(out_dir, "acc_pts_{}.json".format(culm_n_pts))
    gmw_acc_stats_csv = os.path.join(out_dir, "acc_pts_{}.csv".format(culm_n_pts))
    rsgislib.classification.classaccuracymetrics.calc_acc_ptonly_metrics_vecsamples(vec_file=c_pts_vec_file, vec_lyr=c_pts_vec_lyr, ref_col="chng_ref", cls_col="chng_cls", out_json_file=gmw_acc_stats_json, out_csv_file=gmw_acc_stats_csv)

    c_acc_stats_dict = rsgislib.tools.utils.read_json_to_dict(gmw_acc_stats_json)
    acc_stats_dict["Mangroves"].append(c_acc_stats_dict["Mangroves"])
    if "Mangroves > Not Mangroves" in c_acc_stats_dict:
        acc_stats_dict["Mangroves > Not Mangroves"].append(c_acc_stats_dict["Mangroves > Not Mangroves"])
    else:
        tmp_stats = dict()
        tmp_stats["f1-score"] = 0.0
        tmp_stats["precision"] = 0.0
        tmp_stats["recall"] = 0.0
        tmp_stats["support"] = 0.0
        acc_stats_dict["Mangroves > Not Mangroves"].append(tmp_stats)
    acc_stats_dict["Not Mangroves"].append(c_acc_stats_dict["Not Mangroves"])
    if "Not Mangroves > Mangroves" in c_acc_stats_dict:
        acc_stats_dict["Not Mangroves > Mangroves"].append(c_acc_stats_dict["Not Mangroves > Mangroves"])
    else:
        tmp_stats = dict()
        tmp_stats["f1-score"] = 0.0
        tmp_stats["precision"] = 0.0
        tmp_stats["recall"] = 0.0
        tmp_stats["support"] = 0.0
        acc_stats_dict["Not Mangroves > Mangroves"].append(tmp_stats)
    acc_stats_dict["Overall"].append(c_acc_stats_dict["accuracy"])
    culm_n_pts_lst.append(culm_n_pts)

#print(acc_stats_dict["Overall"])
#print(culm_n_pts_lst)

out_info = dict()
out_info["n_pts"] = culm_n_pts_lst
out_info["acc_stats"] = acc_stats_dict

rsgislib.tools.utils.write_dict_to_json(out_info, "gmw_chng_acc_stats_pt_smpls.json")

