import glob
import os
from typing import Dict

import pandas
import geopandas
import numpy

import rsgislib.vectorutils

def count_feats_per_att_val(
    vec_file: str,
    vec_lyr: str,
    col_name: str,
    out_df_dict: bool=False,
) -> Dict:
    """
    A function which returns the count of features for each variable
    value.

    :param vec_file: Input vector file.
    :param vec_lyr: Input vector layer within the input file.
    :param col_name: The column used to count the number of features per value.
    :param out_df_dict: if true then dict will be formatted to import into a
                        pandas dataframe. Otherwise, the output dict will use
                        the attribute values as the key and count as value.
    :return: either dict with keys of vals and count for import into pandas or
             with attribute value and number of features

    """
    import geopandas

    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
    unq_vals = base_gpdf[col_name].unique()

    out_dict = dict()
    for val in unq_vals:
        c_gpdf = base_gpdf.loc[base_gpdf[col_name] == val]
        out_dict[val] = len(c_gpdf)

    if out_df_dict:
        blt_df_dict = dict()
        blt_df_dict["vals"] = list()
        blt_df_dict["count"] = list()

        for val in out_dict:
            blt_df_dict["vals"].append(val)
            blt_df_dict["count"].append(out_dict[val])
        out_dict = blt_df_dict

    return out_dict

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

for pt_set_file in acc_set_vld_files:
    print(pt_set_file)
    vec_lyr = rsgislib.vectorutils.get_vec_lyrs_lst(pt_set_file)[0]
    out_counts = count_feats_per_att_val(pt_set_file, vec_lyr, "chng_ref", True)
    df = pandas.DataFrame.from_dict(out_counts)
    df = df.set_index("vals")
    print(df)
    print("\n\n\n")

"""
blt_df_dict = dict()
blt_df_dict["vals"] = list()
blt_df_dict["count"] = list()

for val in out_counts:
    blt_df_dict["vals"].append(val)
    blt_df_dict["count"].append(out_counts[val])
"""

