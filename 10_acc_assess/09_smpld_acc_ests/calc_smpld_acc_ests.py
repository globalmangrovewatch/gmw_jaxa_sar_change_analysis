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
    ref_smpls = params[1]
    pred_smpls = params[2]
    n_smpls = params[3]
    out_file = params[4]

    idxs = numpy.arange(0, ref_smpls.shape[0], 1)
    sub_idxs = numpy.random.choice(idxs, n_smpls, replace=False)

    ref_smpls_sub = ref_smpls[sub_idxs]
    pred_smpls_sub = pred_smpls[sub_idxs]

    acc_stats = calc_class_pt_accuracy_metrics(ref_smpls_sub, pred_smpls_sub, cls_lst)

    write_dict_to_json(acc_stats, out_file)


def run(n_sites, out_base):
    ref_dir = "../00_data/04_ref_samples"

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

    ref_smpls_df = pandas.concat(df_lst).astype(str)

    ref_smpls_df.sample(frac=1, random_state=42).reset_index(drop=True)

    ref_smpls = ref_smpls_df["ref"].values
    pred_smpls = ref_smpls_df["pred"].values

    print(ref_smpls.shape)
    print(pred_smpls.shape)

    cls_lst = numpy.array(["Mangroves", "Not Mangroves", "Mangroves > Not Mangroves", "Not Mangroves > Mangroves"])

    smpls = [1000, 2500, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 75000, 100000]
    params = []
    for smpl in smpls:
        out_file = f"{out_base}_{smpl}.json"
        params.append([cls_lst, ref_smpls, pred_smpls, smpl, out_file])

    with Pool(12) as p:
        p.map(run_smpld_acc, params)


parser = argparse.ArgumentParser(description='Process Samples...')
parser.add_argument('--nsites', type=int, help='n site files.')
parser.add_argument('--outbase', type=str, help='output base file.')

args = parser.parse_args()

run(args.nsites, args.outbase)
