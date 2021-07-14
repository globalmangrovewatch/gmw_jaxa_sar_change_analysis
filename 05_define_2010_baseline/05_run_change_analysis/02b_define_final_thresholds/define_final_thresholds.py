import os
import numpy
import pandas

def readJSON2Dict(input_file):
    """
    Read a JSON file. Will return a list or dict.

    :param input_file: input JSON file path.

    """
    import json
    with open(input_file) as f:
        data = json.load(f)
    return data

def writeDict2JSON(data_dict, out_file):
    """
    Write some data to a JSON file. The data would commonly be structured as a dict but could also be a list.

    :param data_dict: The dict (or list) to be written to the output JSON file.
    :param out_file: The file path to the output file.

    """
    import json
    with open(out_file, 'w') as fp:
        json.dump(data_dict, fp, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


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


prj_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_projects_luts.json"
prj_lut_dict = readJSON2Dict(prj_lut_file)
prj_idx_lst = list(prj_lut_dict.keys())

thres_base_dir = "/Users/pete/Temp/gmw_v3_analysis/v3_2010_refine_chng_thresholds/outputs/gmw_2010_2010_prj_thres"
out_dir = "/Users/pete/Temp/gmw_v3_analysis/v3_2010_refine_chng_thresholds/"
prj_chng_thres_dir = "/Users/pete/Temp/gmw_v3_analysis/v3_2010_refine_chng_thresholds/outputs/fnl_prj_thresholds"

#thres_base_dir = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/"
#out_dir = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/fnl_prj_thresholds"
#prj_chng_thres_dir = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/fnl_prj_thresholds"

mng_hh = list()
mng_hh_se = list()
mng_hv = list()
mng_hv_se = list()
nmng_hh = list()
nmng_hh_se = list()
nmng_hv = list()
nmng_hv_se = list()

mng_hh_median = list()
mng_hh_se_median = list()
mng_hv_median = list()
mng_hv_se_median = list()
nmng_hh_median = list()
nmng_hh_se_median = list()
nmng_hv_median = list()
nmng_hv_se_median = list()

for prj in prj_idx_lst:
    print(prj)

    fnl_chng_thres_file = os.path.join(prj_chng_thres_dir, "{}_fnl_thresholds.json".format(prj))
    prj_chng_fnl_thresholds = readJSON2Dict(fnl_chng_thres_file)

    mng_hh_median.append(prj_chng_fnl_thresholds["mng_hh_median"])
    mng_hh_se_median.append(prj_chng_fnl_thresholds["mng_hh_se_median"])
    mng_hv_median.append(prj_chng_fnl_thresholds["mng_hv_median"])
    mng_hv_se_median.append(prj_chng_fnl_thresholds["mng_hv_se_median"])
    nmng_hh_median.append(prj_chng_fnl_thresholds["nmng_hh_median"])
    nmng_hh_se_median.append(prj_chng_fnl_thresholds["nmng_hh_se_median"])
    nmng_hv_median.append(prj_chng_fnl_thresholds["nmng_hv_median"])
    nmng_hv_se_median.append(prj_chng_fnl_thresholds["nmng_hv_se_median"])

    prj_thres_file = findFileNone(thres_base_dir, "{}*_chng_thres.json".format(prj))
    if prj_thres_file is not None:
        prj_thresholds = readJSON2Dict(prj_thres_file)
        if (prj_thresholds['his_mng_hh'] < 0) and (prj_thresholds['his_mng_hh'] > prj_thresholds['yen_mng_hh']):
            mng_hh.append(prj_thresholds['his_mng_hh'])
            mng_hh_se.append(prj_thresholds['his_mng_hh_se'])

        else:
            mng_hh.append(prj_thresholds['yen_mng_hh'])
            mng_hh_se.append(prj_thresholds['yen_mng_hh_se'])

        if (prj_thresholds['his_mng_hv'] < 0) and (prj_thresholds['his_mng_hv'] > prj_thresholds['yen_mng_hv']):
            mng_hv.append(prj_thresholds['his_mng_hv'])
            mng_hv_se.append(prj_thresholds['his_mng_hv_se'])
        else:
            mng_hv.append(prj_thresholds['yen_mng_hv'])
            mng_hv_se.append(prj_thresholds['yen_mng_hv_se'])

        if (prj_thresholds['yen_nmng_hh'] < 0) and (prj_thresholds['his_nmng_hh'] < prj_thresholds['yen_nmng_hh']):
            nmng_hh.append(prj_thresholds['his_nmng_hh'])
            nmng_hh_se.append(prj_thresholds['his_nmng_hh_se'])
        else:
            nmng_hh.append(prj_thresholds['yen_nmng_hh'])
            nmng_hh_se.append(prj_thresholds['yen_nmng_hh_se'])

        if (prj_thresholds['yen_nmng_hv'] < 0) and (prj_thresholds['his_nmng_hv'] < prj_thresholds['yen_nmng_hv']):
            nmng_hv.append(prj_thresholds['his_nmng_hv'])
            nmng_hv_se.append(prj_thresholds['his_nmng_hv_se'])
        else:
            nmng_hv.append(prj_thresholds['yen_nmng_hv'])
            nmng_hv_se.append(prj_thresholds['yen_nmng_hv_se'])
    else:
        mng_hh.append(0.0)
        mng_hh_se.append(0.0)
        mng_hv.append(0.0)
        mng_hv_se.append(0.0)
        nmng_hh.append(0.0)
        nmng_hh_se.append(0.0)
        nmng_hv.append(0.0)
        nmng_hv_se.append(0.0)

mng_hh_fnl = list()
mng_hh_se_fnl = list()
for i in range(len(mng_hh)):
    if abs(mng_hh[i] - mng_hh_median[i]) > 200:
        mng_hh_fnl.append(mng_hh_median[i])
        mng_hh_se_fnl.append(mng_hh_se_median[i])
    else:
        mng_hh_fnl.append(mng_hh[i])
        mng_hh_se_fnl.append(mng_hh_se[i])

mng_hv_fnl = list()
mng_hv_se_fnl = list()
for i in range(len(mng_hv)):
    if abs(mng_hv[i] - mng_hv_median[i]) > 200:
        mng_hv_fnl.append(mng_hv_median[i])
        mng_hv_se_fnl.append(mng_hv_se_median[i])
    else:
        mng_hv_fnl.append(mng_hv[i])
        mng_hv_se_fnl.append(mng_hv_se[i])

nmng_hh_fnl = list()
nmng_hh_se_fnl = list()
for i in range(len(nmng_hh)):
    if abs(nmng_hh[i] - nmng_hh_median[i]) > 200:
        nmng_hh_fnl.append(nmng_hh_median[i])
        nmng_hh_se_fnl.append(nmng_hh_se_median[i])
    else:
        nmng_hh_fnl.append(nmng_hh[i])
        nmng_hh_se_fnl.append(nmng_hh_se[i])

nmng_hv_fnl = list()
nmng_hv_se_fnl = list()
for i in range(len(nmng_hv)):
    if abs(nmng_hv[i] - nmng_hv_median[i]) > 200:
        nmng_hv_fnl.append(nmng_hv_median[i])
        nmng_hv_se_fnl.append(nmng_hv_se_median[i])
    else:
        nmng_hv_fnl.append(nmng_hv[i])
        nmng_hv_se_fnl.append(nmng_hv_se[i])

out_thresholds = dict()
out_thresholds['Project'] = prj_idx_lst

out_thresholds['mng_hh_fnl'] = numpy.array(mng_hh_fnl)/100.0
out_thresholds['mng_hh_se_fnl'] = numpy.array(mng_hh_se_fnl)/100.0
out_thresholds['mng_hv_fnl'] = numpy.array(mng_hv_fnl)/100.0
out_thresholds['mng_hv_se_fnl'] = numpy.array(mng_hv_se_fnl)/100.0
out_thresholds['nmng_hh_fnl'] = numpy.array(nmng_hh_fnl)/100.0
out_thresholds['nmng_hh_se_fnl'] = numpy.array(nmng_hh_se_fnl)/100.0
out_thresholds['nmng_hv_fnl'] = numpy.array(nmng_hv_fnl)/100.0
out_thresholds['nmng_hv_se_fnl'] = numpy.array(nmng_hv_se_fnl)/100.0

out_thresholds['mng_hh'] = numpy.array(mng_hh)/100.0
out_thresholds['mng_hh_se'] = numpy.array(mng_hh_se)/100.0
out_thresholds['mng_hv'] = numpy.array(mng_hv)/100.0
out_thresholds['mng_hv_se'] = numpy.array(mng_hv_se)/100.0
out_thresholds['nmng_hh'] = numpy.array(nmng_hh)/100.0
out_thresholds['nmng_hh_se'] = numpy.array(nmng_hh_se)/100.0
out_thresholds['nmng_hv'] = numpy.array(nmng_hv)/100.0
out_thresholds['nmng_hv_se'] = numpy.array(nmng_hv_se)/100.0

out_thresholds['mng_hh_median'] = numpy.array(mng_hh_median)/100.0
out_thresholds['mng_hh_se_median'] = numpy.array(mng_hh_se_median)/100.0
out_thresholds['mng_hv_median'] = numpy.array(mng_hv_median)/100.0
out_thresholds['mng_hv_se_median'] = numpy.array(mng_hv_se_median)/100.0
out_thresholds['nmng_hh_median'] = numpy.array(nmng_hh_median)/100.0
out_thresholds['nmng_hh_se_median'] = numpy.array(nmng_hh_se_median)/100.0
out_thresholds['nmng_hv_median'] = numpy.array(nmng_hv_median)/100.0
out_thresholds['nmng_hv_se_median'] = numpy.array(nmng_hv_se_median)/100.0


df_prj_thresholds = pandas.DataFrame.from_dict(out_thresholds)

xls_writer = pandas.ExcelWriter('gmw_2010_chng_thresholds.xlsx', engine='xlsxwriter')
df_prj_thresholds.to_excel(xls_writer, sheet_name=prj)
xls_writer.save()

out_lut_dict = dict()
for i in range(len(prj_idx_lst)):
    prj = prj_idx_lst[i]
    print(prj)
    out_lut_dict[prj] = dict()
    out_lut_dict[prj]["mng_hh"] = mng_hh_fnl[i]
    out_lut_dict[prj]["mng_hh_se"] = mng_hh_se_fnl[i]
    out_lut_dict[prj]["mng_hv"] = mng_hv_fnl[i]
    out_lut_dict[prj]["mng_hv_se"] = mng_hv_se_fnl[i]
    out_lut_dict[prj]["nmng_hh"] = nmng_hh_fnl[i]
    out_lut_dict[prj]["nmng_hh_se"] = nmng_hh_se_fnl[i]
    out_lut_dict[prj]["nmng_hv"] = nmng_hv_fnl[i]
    out_lut_dict[prj]["nmng_hv_se"] = nmng_hv_se_fnl[i]

writeDict2JSON(out_lut_dict, "gmw_2010_fnl_thresholds_lut.json")