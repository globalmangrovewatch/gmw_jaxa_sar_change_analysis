import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../06_run_acc_mdls')

from classaccuracymetrics import create_modelled_acc_pts, calc_sampled_acc_metrics, create_norm_modelled_err_matrix
import numpy
import pandas
import os
import tqdm
import rsgislib.tools.utils

def get_base_chng_years(years, np_rng):
    found = False
    base_year = np_rng.choice(years[:-1])
    while not found:
        chng_year = np_rng.choice(years)
        if chng_year > base_year:
            found = True
            break
    return base_year, chng_year


acc_ref_smpls = rsgislib.tools.utils.read_json_to_dict("../05_get_site_statistics/ref_smpl_acc_set.json")
cls_props_sets = rsgislib.tools.utils.read_json_to_dict("../05_get_site_statistics/site_chng_pxl_counts.json")

acc_smpl_idxs = numpy.arange(0, 250, 1)
site_ids = numpy.arange(1, 38, 1)

gmw_years = [1996, 2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]

cls_lst = ["Mangroves", "Not Mangroves", "Mangroves > Not Mangroves", "Not Mangroves > Mangroves"]

cls_clrs = dict()
cls_clrs["Mangroves"] = [0.0, 1.0, 0.0]
cls_clrs["Not Mangroves"] = [0.2, 0.2, 0.2]
cls_clrs["Mangroves > Not Mangroves"] = [1.0, 0.0, 0.0]
cls_clrs["Not Mangroves > Mangroves"] = [0.0, 0.0, 1.0]

out_dir = "../00_data/04_ref_samples"

np_rng = numpy.random.default_rng(seed=42)

for i in tqdm.tqdm(range(100)):
    site_id = np_rng.choice(site_ids)
    base_year, chng_year = get_base_chng_years(gmw_years, np_rng)
    cls_key = f"{site_id}_b{base_year}_c{chng_year}"

    acc_ref_smpls_id = np_rng.choice(acc_smpl_idxs)
    cls_prop_info = cls_props_sets[cls_key]
    smpl_ref_acc = acc_ref_smpls[f"{acc_ref_smpls_id}"]

    cls_props = cls_prop_info["cls_prop"]
    n_smpls = int(cls_prop_info["total"])

    err_mtx = create_norm_modelled_err_matrix(cls_props, smpl_ref_acc)
    ref_samples, pred_samples = create_modelled_acc_pts(err_mtx, cls_lst, n_smpls)

    out_file = os.path.join(out_dir, f"site_{cls_key}.feather")

    smpls_dict = dict()
    smpls_dict["ref"] = ref_samples
    smpls_dict["pred"] = pred_samples

    smpls_df = pandas.DataFrame.from_dict(smpls_dict)
    smpls_df.to_feather(out_file)
