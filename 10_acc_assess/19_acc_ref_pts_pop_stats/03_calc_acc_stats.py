
import glob
import rsgislib.classification.classaccuracymetrics
import rsgislib.vectorutils

from typing import Union, List, Dict


def find_replace_str_vec_lyr(
    vec_file: str,
    vec_lyr: str,
    out_vec_file: str,
    out_vec_lyr: str,
    cols: List[str],
    find_replace: Dict[str, str],
    out_format: str = "GPKG",
):
    """
    A function which performs a find and replace on a string column(s) within the
    vector layer. For example, replacing a no data value (e.g., NA) with something
    more useful. This function is implemented using geopandas.

    :param vec_file: the input vector file.
    :param vec_lyr: the input vector layer name.
    :param out_vec_file: the output vector file.
    :param out_vec_lyr: the output vector layer name.
    :param cols: a list of strings with the names of the columns to which
                 the find and replace is to be applied.
    :param find_replace: the value pairs where the dict keys are the values
                         to be replaced and the value is the replacement
                         value.
    :param out_format: The output vector file format (Default: GPKG)

    """
    import geopandas

    # Read input vector file.
    base_gpdf = geopandas.read_file(vec_file, layer=vec_lyr)

    # Perform find and replace
    for col in cols:
        for find_val in find_replace:
            base_gpdf[col] = base_gpdf[col].str.replace(find_val, find_replace[find_val])

    if out_format == "GPKG":
        base_gpdf.to_file(out_vec_file, layer=out_vec_lyr, driver=out_format)
    else:
        base_gpdf.to_file(out_vec_file, driver=out_format)






acc_ref_pt_files = glob.glob("acc_ref_pts/*.geojson")
acc_chng_pt_files = glob.glob("acc_chng_pts/*.geojson")

acc_pt_files = acc_chng_pt_files + acc_ref_pt_files

gmw_all_acc_pts = "gmw_chng_ref_acc_pts.geojson"
rsgislib.vectorutils.merge_vector_files(
    vec_files = acc_pt_files,
    out_vec_file = gmw_all_acc_pts,
    out_vec_lyr = None,
    out_format = "GeoJSON",
    out_epsg = None,
)

cols = ["v312_cls", "v313_cls", "v314_cls", "v315_cls"]
replace_vals = {"NA": "Not Mangroves"}
gmw_all_acc_pts_vld = "gmw_chng_ref_acc_pts_vld.geojson"
find_replace_str_vec_lyr(gmw_all_acc_pts, "gmw_chng_ref_acc_pts", gmw_all_acc_pts_vld, "gmw_chng_ref_acc_pts_vld", cols, replace_vals, out_format="GeoJSON")


versions = ["312", "313", "314", "315"]

for version in versions:
    print(version)

    gmw_acc_stats_json = f"gmw_chng_acc_stats_v{version}.json"
    gmw_acc_stats_csv = f"gmw_chng_acc_stats_v{version}.csv"
    rsgislib.classification.classaccuracymetrics.calc_acc_ptonly_metrics_vecsamples(vec_file=gmw_all_acc_pts_vld, vec_lyr="gmw_chng_ref_acc_pts_vld", ref_col="chng_ref", cls_col=f"v{version}_cls", out_json_file=gmw_acc_stats_json, out_csv_file=gmw_acc_stats_csv)

    gmw_acc_stats_conf_json = f"gmw_chng_acc_stats_conf_int_v{version}.json"
    acc_vals = rsgislib.classification.classaccuracymetrics.calc_acc_ptonly_metrics_vecsamples_bootstrap_conf_interval(
        vec_file=gmw_all_acc_pts_vld, vec_lyr="gmw_chng_ref_acc_pts_vld", ref_col="chng_ref", cls_col=f"v{version}_cls",
        out_json_file=gmw_acc_stats_conf_json,
        sample_n_smps=15000,
        bootstrap_n=1000)


