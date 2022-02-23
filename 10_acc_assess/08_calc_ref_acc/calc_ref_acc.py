import glob
import os
import pandas
import numpy
import tqdm

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../06_run_acc_mdls')

from classaccuracymetrics import calc_class_pt_accuracy_metrics

from rsgislib.tools.utils import write_dict_to_json

ref_dir = "../00_data/04_ref_samples"

ref_smpl_files = glob.glob(os.path.join(ref_dir, "*.feather"))

df_lst = list()
for ref_smpl_file in tqdm.tqdm(ref_smpl_files):
    #print(ref_smpl_file)
    ref_smpls_df = pandas.read_feather(ref_smpl_file)
    ref_smpls_df["ref"] = ref_smpls_df["ref"].str.decode('utf-8')
    ref_smpls_df["pred"] = ref_smpls_df["pred"].str.decode('utf-8')
    df_lst.append(ref_smpls_df)

ref_smpls_df = pandas.concat(df_lst).astype(str)

ref_smpls = ref_smpls_df["ref"].values
pref_smpls = ref_smpls_df["pred"].values

print(ref_smpls.shape)
print(pref_smpls.shape)

cls_lst = numpy.array(["Mangroves", "Not Mangroves", "Mangroves > Not Mangroves", "Not Mangroves > Mangroves"])

acc_stats = calc_class_pt_accuracy_metrics(ref_smpls, pref_smpls, cls_lst)

write_dict_to_json(acc_stats, "ref_acc_stats.json")
