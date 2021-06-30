import pandas
import geopandas
import os

def readJSON2Dict(input_file):
    """
    Read a JSON file. Will return a list or dict.

    :param input_file: input JSON file path.

    """
    import json
    with open(input_file) as f:
        data = json.load(f)
    return data

def findFileNone(dirPath, fileSearch):
    """
    Search for a single file with a path using glob. Therefore, the file
    path returned is a true path. Within the fileSearch provide the file
    name with '*' as wildcard(s). Returns None is not found.

    :return: string

    """
    import glob
    import os.path
    files = glob.glob(os.path.join(dirPath, fileSearch))
    if len(files) != 1:
        return None
    return files[0]

def get_year_named(years, pre_append):
    out_lst = []
    for year in years:
        out_lst.append("{}_{}".format(pre_append, year))
    return out_lst

prj_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_projects_luts.json"
prj_lut_dict = readJSON2Dict(prj_lut_file)
prj_idx_lst = prj_lut_dict.keys()

mng_hh_n = list()
nmng_hh_n = list()
mng_hv_n = list()
nmng_hv_n = list()

his_mng_hh = list()
his_nmng_hh = list()
his_mng_hv = list()
his_nmng_hv = list()

yen_mng_hh = list()
yen_nmng_hh = list()
yen_mng_hv = list()
yen_nmng_hv = list()

vars = ['mng_hh_n', 'nmng_hh_n', 'mng_hv_n', 'nmng_hv_n', 'his_mng_hh', 'his_nmng_hh', 'his_mng_hv', 'his_nmng_hv', 'yen_mng_hh', 'yen_nmng_hh', 'yen_mng_hv', 'yen_nmng_hv']

for prj in prj_idx_lst:
    print(prj)
    thres_file = '/Users/pete/Temp/gmw_v3_analysis/glb_thresholds/outputs/{}_glb_chng_thres.json'.format(prj)

    if os.path.exists(thres_file):
        thres_dict = readJSON2Dict(thres_file)

        # Pixel numbers.
        if 'mng_hh_n' in thres_dict:
            mng_hh_n.append(thres_dict['mng_hh_n'])
        else:
            mng_hh_n.append(0)

        if 'nmng_hh_n' in thres_dict:
            nmng_hh_n.append(thres_dict['nmng_hh_n'])
        else:
            nmng_hh_n.append(0)

        if 'mng_hv_n' in thres_dict:
            mng_hv_n.append(thres_dict['mng_hv_n'])
        else:
            mng_hv_n.append(0)

        if 'nmng_hv_n' in thres_dict:
            nmng_hv_n.append(thres_dict['nmng_hv_n'])
        else:
            nmng_hv_n.append(0)

        # Histogram Thresholds
        if 'his_mng_hh' in thres_dict:
            his_mng_hh.append(thres_dict['his_mng_hh']/100.0)
        else:
            his_mng_hh.append(0)

        if 'his_nmng_hh' in thres_dict:
            his_nmng_hh.append(thres_dict['his_nmng_hh']/100.0)
        else:
            his_nmng_hh.append(0)

        if 'his_mng_hv' in thres_dict:
            his_mng_hv.append(thres_dict['his_mng_hv']/100.0)
        else:
            his_mng_hv.append(0)

        if 'his_nmng_hv' in thres_dict:
            his_nmng_hv.append(thres_dict['his_nmng_hv']/100.0)
        else:
            his_nmng_hv.append(0)

        # Yen Thresholds
        if 'yen_mng_hh' in thres_dict:
            yen_mng_hh.append(thres_dict['yen_mng_hh']/100.0)
        else:
            yen_mng_hh.append(0)

        if 'yen_nmng_hh' in thres_dict:
            yen_nmng_hh.append(thres_dict['yen_nmng_hh']/100.0)
        else:
            yen_nmng_hh.append(0)

        if 'yen_mng_hv' in thres_dict:
            yen_mng_hv.append(thres_dict['yen_mng_hv']/100.0)
        else:
            yen_mng_hv.append(0)

        if 'yen_nmng_hv' in thres_dict:
            yen_nmng_hv.append(thres_dict['yen_nmng_hv']/100.0)
        else:
            yen_nmng_hv.append(0)
    else:
        mng_hh_n.append(0)
        nmng_hh_n.append(0)
        mng_hv_n.append(0)
        nmng_hv_n.append(0)

        his_mng_hh.append(0)
        his_nmng_hh.append(0)
        his_mng_hv.append(0)
        his_nmng_hv.append(0)

        yen_mng_hh.append(0)
        yen_nmng_hh.append(0)
        yen_mng_hv.append(0)
        yen_nmng_hv.append(0)


out_vals = dict()
out_vals['Project'] = prj_idx_lst

out_vals['mng_hh_n'] = mng_hh_n
out_vals['nmng_hh_n'] = nmng_hh_n
out_vals['mng_hv_n'] = mng_hv_n
out_vals['nmng_hv_n'] = nmng_hv_n

out_vals['his_mng_hh'] = his_mng_hh
out_vals['his_nmng_hh'] = his_nmng_hh
out_vals['his_mng_hv'] = his_mng_hv
out_vals['his_nmng_hv'] = his_nmng_hv

out_vals['yen_mng_hh'] = yen_mng_hh
out_vals['yen_nmng_hh'] = yen_nmng_hh
out_vals['yen_mng_hv'] = yen_mng_hv
out_vals['yen_nmng_hv'] = yen_nmng_hv

df_glb = pandas.DataFrame.from_dict(out_vals, orient='columns')
df_glb.set_index('Project')

for var in vars:
    df_glb.loc[(df_glb[var] == 0), var] = None

# Create a Pandas Excel writer using XlsxWriter as the engine.
xls_writer = pandas.ExcelWriter('gmw_glb_chng_thresholds.xlsx', engine='xlsxwriter')

df_glb.to_excel(xls_writer, sheet_name='global_threshold')

xls_writer.save()

