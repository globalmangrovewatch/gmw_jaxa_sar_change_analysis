import glob
import os
import math
from typing import Union, List

import rsgislib.vectorutils


def sort_vec_lyr(vec_file:str, vec_lyr:str, out_vec_file:str, out_vec_lyr:str, sort_by:Union[str, List[str]], ascending:Union[bool, List[bool]], out_format: str = "GPKG"):
    """
    A function which sorts a vector layer based on the attributes of the layer.
    You can sort by either a single attribute or within multiple attributes
    if a list is provided. This function is implemented using geopandas.

    :param vec_file: the input vector file.
    :param vec_lyr: the input vector layer name.
    :param out_vec_file: the output vector file.
    :param out_vec_lyr: the output vector layer name.
    :param sort_by: either a string with the name of a single attribute or a list
                    of strings if multiple attributes are used for the sort.
    :param ascending: either a bool (True: ascending; False: descending) or list
                      of bools if a list of attributes was given.
    :param out_format: The output vector file format (Default: GPKG)

    """
    import geopandas

    if type(sort_by) is list:
        if type(ascending) is not list:
            raise rsgislib.RSGISPyException("If sort_by is a list then ascending must be too.")

        if len(sort_by) != len(ascending):
            raise rsgislib.RSGISPyException("If lists, the length of sort_by and ascending must be the same.")

    # Read input vector file.
    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)

    # sort layer.
    sorted_gpdf = base_gpdf.sort_values(by=sort_by, ascending=ascending)

    if out_format == "GPKG":
        sorted_gpdf.to_file(out_vec_file, layer=out_vec_lyr, driver=out_format)
    else:
        sorted_gpdf.to_file(out_vec_file, driver=out_format)


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


set1_sort_out_dir = "acc_chng_pts_set_1_sort"
if not os.path.exists(set1_sort_out_dir):
    os.mkdir(set1_sort_out_dir)

set2_sort_out_dir = "acc_chng_pts_set_2_sort"
if not os.path.exists(set2_sort_out_dir):
    os.mkdir(set2_sort_out_dir)

set3_sort_out_dir = "acc_chng_pts_set_3_sort"
if not os.path.exists(set3_sort_out_dir):
    os.mkdir(set3_sort_out_dir)

set4_sort_out_dir = "acc_chng_pts_set_4_sort"
if not os.path.exists(set4_sort_out_dir):
    os.mkdir(set4_sort_out_dir)


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

    set1_sort_out_vec_lyr = f"{input_acc_pts_lyr}_set1"
    set1_sort_out_vec_file = os.path.join(set1_sort_out_dir, f"{set1_out_vec_lyr}.geojson")
    sort_vec_lyr(set1_out_vec_file, set1_out_vec_lyr, set1_sort_out_vec_file, set1_sort_out_vec_lyr, sort_by="chng_cls", ascending=True, out_format="GeoJSON")

    set2_sort_out_vec_lyr = f"{input_acc_pts_lyr}_set2"
    set2_sort_out_vec_file = os.path.join(set2_sort_out_dir, f"{set2_out_vec_lyr}.geojson")
    sort_vec_lyr(set2_out_vec_file, set2_out_vec_lyr, set2_sort_out_vec_file, set2_sort_out_vec_lyr, sort_by="chng_cls", ascending=True, out_format="GeoJSON")

    set3_sort_out_vec_lyr = f"{input_acc_pts_lyr}_set3"
    set3_sort_out_vec_file = os.path.join(set3_sort_out_dir, f"{set3_out_vec_lyr}.geojson")
    sort_vec_lyr(set3_out_vec_file, set3_out_vec_lyr, set3_sort_out_vec_file, set3_sort_out_vec_lyr, sort_by="chng_cls", ascending=True, out_format="GeoJSON")

    set4_sort_out_vec_lyr = f"{input_acc_pts_lyr}_set4"
    set4_sort_out_vec_file = os.path.join(set4_sort_out_dir, f"{set4_out_vec_lyr}.geojson")
    sort_vec_lyr(set4_out_vec_file, set4_out_vec_lyr, set4_sort_out_vec_file, set4_sort_out_vec_lyr, sort_by="chng_cls", ascending=True, out_format="GeoJSON")


