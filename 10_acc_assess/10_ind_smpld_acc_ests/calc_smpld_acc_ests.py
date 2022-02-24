import glob
import os
import pandas
import numpy
import tqdm
import argparse
from multiprocessing import Pool
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../06_run_acc_mdls')

from classaccuracymetrics import calc_class_pt_accuracy_metrics

from rsgislib.tools.utils import write_dict_to_json


def run_smpld_acc(params):
    cls_lst = params[0]
    df_lst = params[1]
    n_smpls = params[2]
    out_file = params[3]

    df_smpl_lst = list()
    for df_smpl in df_lst:
        df_smpl_lst.append(df_smpl.sample(n=n_smpls))

    ref_smpls_df = pandas.concat(df_smpl_lst).astype(str)

    ref_smpls_sub = ref_smpls_df["ref"].values
    pred_smpls_sub = ref_smpls_df["pred"].values

    #print(ref_smpls_sub.shape)
    #print(pred_smpls_sub.shape)

    acc_stats = calc_class_pt_accuracy_metrics(ref_smpls_sub, pred_smpls_sub, cls_lst)

    write_dict_to_json(acc_stats, out_file)


def run(n_sites, out_dir):
    ref_dir = "../00_data/04_ref_samples"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    out_base = os.path.join(out_dir, f"sites_{n_sites}")

    ref_smpl_files = glob.glob(os.path.join(ref_dir, "*.feather"))

    site_idxs = numpy.arange(0, len(ref_smpl_files), 1)
    site_sub_idxs = numpy.random.choice(site_idxs, n_sites, replace=False)
    ref_smpl_files_arr = numpy.array(ref_smpl_files)
    ref_smpl_files_arr = ref_smpl_files_arr[site_sub_idxs]

    df_lst = list()
    for ref_smpl_file in tqdm.tqdm(ref_smpl_files_arr):
        #print(ref_smpl_file)
        ref_smpls_df = pandas.read_feather(ref_smpl_file)
        ref_smpls_df["ref"] = ref_smpls_df["ref"].str.decode('utf-8')
        ref_smpls_df["pred"] = ref_smpls_df["pred"].str.decode('utf-8')
        df_lst.append(ref_smpls_df)

    cls_lst = numpy.array(["Mangroves", "Not Mangroves", "Mangroves > Not Mangroves", "Not Mangroves > Mangroves"])

    smpls = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    params = []
    for smpl in smpls:
        out_file = f"{out_base}_{smpl}.json"
        params.append([cls_lst, df_lst, smpl, out_file])

    with Pool(15) as p:
        p.map(run_smpld_acc, params)


parser = argparse.ArgumentParser(description='Process Samples...')
parser.add_argument('--nsites', type=int, required=True, help='n site files.')
parser.add_argument('--outdir', type=str, required=True, help='output base file.')

args = parser.parse_args()

run(args.nsites, args.outdir)
