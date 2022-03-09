import glob
import os
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


set_in_dir = "acc_ref_pts_set_1"
set_out_dir = "acc_ref_pts_set_1_sorted"

input_acc_pts_files = glob.glob(os.path.join(set_in_dir, "*.geojson"))
for input_acc_pts_file in input_acc_pts_files:
    input_acc_pts_lyr = rsgislib.vectorutils.get_vec_lyrs_lst(input_acc_pts_file)[0]

    out_vec_lyr = input_acc_pts_lyr
    out_vec_file = os.path.join(set_out_dir, f"{out_vec_lyr}.geojson")

    sort_vec_lyr(input_acc_pts_file, input_acc_pts_lyr, out_vec_file, out_vec_lyr, sort_by="chng_cls", ascending=True, out_format="GeoJSON")

set_in_dir = "acc_ref_pts_set_2"
set_out_dir = "acc_ref_pts_set_2_sorted"

input_acc_pts_files = glob.glob(os.path.join(set_in_dir, "*.geojson"))
for input_acc_pts_file in input_acc_pts_files:
    input_acc_pts_lyr = rsgislib.vectorutils.get_vec_lyrs_lst(input_acc_pts_file)[0]

    out_vec_lyr = input_acc_pts_lyr
    out_vec_file = os.path.join(set_out_dir, f"{out_vec_lyr}.geojson")

    sort_vec_lyr(input_acc_pts_file, input_acc_pts_lyr, out_vec_file, out_vec_lyr, sort_by="chng_cls", ascending=True, out_format="GeoJSON")