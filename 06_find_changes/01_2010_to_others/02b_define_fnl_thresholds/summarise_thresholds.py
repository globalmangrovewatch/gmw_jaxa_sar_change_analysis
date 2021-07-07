import os
import numpy
import pandas
import pprint

def readJSON2Dict(input_file):
    """
    Read a JSON file. Will return a list or dict.

    :param input_file: input JSON file path.

    """
    import json
    with open(input_file) as f:
        data = json.load(f)
    return data


prj_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_projects_luts.json"
prj_lut_dict = readJSON2Dict(prj_lut_file)
prj_idx_lst = prj_lut_dict.keys()

thresholds_dir = "/Users/pete/Temp/gmw_v3_analysis/gmw_chng_thresholds/fnl_thresholds"

# Create a Pandas Excel writer using XlsxWriter as the engine.
xls_writer = pandas.ExcelWriter('gmw_chng_thresholds.xlsx', engine='xlsxwriter')
for prj in prj_idx_lst:
    prj_thres_file = os.path.join(thresholds_dir, "{}_fnl_thresholds.json".format(prj))
    prj_thresholds = readJSON2Dict(prj_thres_file)

    #pprint.pprint(prj_thresholds)

    df_prj_thresholds = pandas.DataFrame.from_dict(prj_thresholds)
    df_prj_thresholds = df_prj_thresholds / 100



    df_prj_thresholds.to_excel(xls_writer, sheet_name=prj)

xls_writer.save()
