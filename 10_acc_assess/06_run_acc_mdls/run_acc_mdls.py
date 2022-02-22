from classaccuracymetrics import create_modelled_acc_pts, calc_sampled_acc_metrics, create_norm_modelled_err_matrix
import numpy
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
cls_clrs["Not Mangroves"] = [0.8, 0.8, 0.8]
cls_clrs["Mangroves to Not Mangroves"] = [1.0, 0.0, 0.0]
cls_clrs["Not Mangroves to Mangroves"] = [0.0, 0.0, 1.0]

out_dir = "../00_data/03_experiment_outputs"

np_rng = numpy.random.default_rng(seed=42)

for i in tqdm.tqdm(range(10)):
    site_id = np_rng.choice(site_ids)
    base_year, chng_year = get_base_chng_years(gmw_years, np_rng)
    cls_key = f"{site_id}_b{base_year}_c{chng_year}"

    acc_ref_smpls_id = np_rng.choice(acc_smpl_idxs)
    cls_prop_info = cls_props_sets[cls_key]
    smpl_ref_acc = acc_ref_smpls[f"{acc_ref_smpls_id}"]

    cls_props = cls_prop_info["cls_prop"]
    n_smpls = cls_prop_info["total"]

    err_mtx = create_norm_modelled_err_matrix(cls_props, smpl_ref_acc)
    ref_samples, pred_samples = create_modelled_acc_pts(err_mtx, cls_lst, n_smpls)

    smpls_lst = [int(n_smpls*0.01), int(n_smpls*0.02), int(n_smpls*0.05), int(n_smpls*0.1), int(n_smpls*0.15), int(n_smpls*0.2), int(n_smpls*0.25), int(n_smpls*0.3), int(n_smpls*0.4), int(n_smpls*0.5), int(n_smpls*0.6)]#, int(n_smpls*0.7), int(n_smpls*0.8), int(n_smpls*0.9)]
    #print(smpls_lst)

    out_metrics_file = os.path.join(out_dir, f"{i}_out_stats.json"),
    out_usr_metrics_plot = os.path.join(out_dir, f"{i}_out_usrs_plot.png"),
    out_prod_metrics_plot = os.path.join(out_dir, f"{i}_out_prod_plot.png"),
    out_ref_usr_plot = os.path.join(out_dir, f"{i}_ref_usr_plot.png"),
    out_ref_prod_plot = os.path.join(out_dir, f"{i}_ref_prod_plot.png"),

    calc_sampled_acc_metrics(ref_samples, pred_samples, cls_lst, smpls_lst,
                             out_metrics_file=out_metrics_file,
                             out_usr_metrics_plot=out_usr_metrics_plot,
                             out_prod_metrics_plot=out_prod_metrics_plot,
                             out_ref_usr_plot=out_ref_usr_plot,
                             out_ref_prod_plot=out_ref_prod_plot,
                             cls_colours=cls_clrs)
