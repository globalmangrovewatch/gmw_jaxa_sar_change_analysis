import os
import numpy

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

def calcFnlPrjThreholds(prj_lut_file, thres_base_dir, out_dir, years, ref_year):

    prj_lut_dict = readJSON2Dict(prj_lut_file)
    prj_idx_lst = prj_lut_dict.keys()

    for prj in prj_idx_lst:
        print(prj)
        prj_thres_files = dict()
        prj_thresholds = dict()
        mng_hh = list()
        mng_hh_se = list()
        mng_hv = list()
        mng_hv_se = list()
        nmng_hh = list()
        nmng_hh_se = list()
        nmng_hv = list()
        nmng_hv_se = list()

        prj_out_thresholds = dict()

        for year in years:
            prj_year_dir = os.path.join(thres_base_dir, "gmw_{}_{}_prj_thres".format(ref_year, year))
            prj_thres_files[year] = findFileNone(prj_year_dir, "{}_{}_chng_thres.json".format(prj, year))
            prj_out_thresholds[year] = dict()
            if prj_thres_files[year] is not None:
                prj_thresholds[year] = readJSON2Dict(prj_thres_files[year])
                if (prj_thresholds[year]['his_mng_hh'] < 0) and (prj_thresholds[year]['his_mng_hh'] > prj_thresholds[year]['yen_mng_hh']):
                    mng_hh.append(prj_thresholds[year]['his_mng_hh'])
                    mng_hh_se.append(prj_thresholds[year]['his_mng_hh_se'])
                    prj_out_thresholds[year]['mng_hh'] = prj_thresholds[year]['his_mng_hh']
                    prj_out_thresholds[year]['mng_hh_se'] = prj_thresholds[year]['his_mng_hh_se']
                else:
                    mng_hh.append(prj_thresholds[year]['yen_mng_hh'])
                    mng_hh_se.append(prj_thresholds[year]['yen_mng_hh_se'])
                    prj_out_thresholds[year]['mng_hh'] = prj_thresholds[year]['yen_mng_hh']
                    prj_out_thresholds[year]['mng_hh_se'] = prj_thresholds[year]['yen_mng_hh_se']

                if (prj_thresholds[year]['his_mng_hv'] < 0) and (prj_thresholds[year]['his_mng_hv'] > prj_thresholds[year]['yen_mng_hv']):
                    mng_hv.append(prj_thresholds[year]['his_mng_hv'])
                    mng_hv_se.append(prj_thresholds[year]['his_mng_hv_se'])
                    prj_out_thresholds[year]['mng_hv'] = prj_thresholds[year]['his_mng_hv']
                    prj_out_thresholds[year]['mng_hv_se'] = prj_thresholds[year]['his_mng_hv_se']
                else:
                    mng_hv.append(prj_thresholds[year]['yen_mng_hv'])
                    mng_hv_se.append(prj_thresholds[year]['yen_mng_hv_se'])
                    prj_out_thresholds[year]['mng_hv'] = prj_thresholds[year]['yen_mng_hv']
                    prj_out_thresholds[year]['mng_hv_se'] = prj_thresholds[year]['yen_mng_hv_se']

                if (prj_thresholds[year]['yen_nmng_hh'] < 0) and (prj_thresholds[year]['his_nmng_hh'] < prj_thresholds[year]['yen_nmng_hh']):
                    nmng_hh.append(prj_thresholds[year]['his_nmng_hh'])
                    nmng_hh_se.append(prj_thresholds[year]['his_nmng_hh_se'])
                    prj_out_thresholds[year]['nmng_hh'] = prj_thresholds[year]['his_nmng_hh']
                    prj_out_thresholds[year]['nmng_hh_se'] = prj_thresholds[year]['his_nmng_hh_se']
                else:
                    nmng_hh.append(prj_thresholds[year]['yen_nmng_hh'])
                    nmng_hh_se.append(prj_thresholds[year]['yen_nmng_hh_se'])
                    prj_out_thresholds[year]['nmng_hh'] = prj_thresholds[year]['yen_nmng_hh']
                    prj_out_thresholds[year]['nmng_hh_se'] = prj_thresholds[year]['yen_nmng_hh_se']

                if (prj_thresholds[year]['yen_nmng_hv'] < 0) and (prj_thresholds[year]['his_nmng_hv'] < prj_thresholds[year]['yen_nmng_hv']):
                    nmng_hv.append(prj_thresholds[year]['his_nmng_hv'])
                    nmng_hv_se.append(prj_thresholds[year]['his_nmng_hv_se'])
                    prj_out_thresholds[year]['nmng_hv'] = prj_thresholds[year]['his_nmng_hv']
                    prj_out_thresholds[year]['nmng_hv_se'] = prj_thresholds[year]['his_nmng_hv_se']
                else:
                    nmng_hv.append(prj_thresholds[year]['yen_nmng_hv'])
                    nmng_hv_se.append(prj_thresholds[year]['yen_nmng_hv_se'])
                    prj_out_thresholds[year]['nmng_hv'] = prj_thresholds[year]['yen_nmng_hv']
                    prj_out_thresholds[year]['nmng_hv_se'] = prj_thresholds[year]['yen_nmng_hv_se']
            else:
                prj_out_thresholds[year]['mng_hh'] = 0.0
                prj_out_thresholds[year]['mng_hh_se'] = 0.0
                prj_out_thresholds[year]['mng_hv'] = 0.0
                prj_out_thresholds[year]['mng_hv_se'] = 0.0
                prj_out_thresholds[year]['nmng_hh'] = 0.0
                prj_out_thresholds[year]['nmng_hh_se'] = 0.0
                prj_out_thresholds[year]['nmng_hv'] = 0.0
                prj_out_thresholds[year]['nmng_hv_se'] = 0.0

        mng_hh_arr = numpy.array(mng_hh)
        mng_hh_arr = mng_hh_arr[mng_hh_arr < 0]
        mng_hh_arr = mng_hh_arr[numpy.isfinite(mng_hh_arr)]
        mng_hh_mean = numpy.mean(mng_hh_arr)
        mng_hh_median = numpy.median(mng_hh_arr)

        mng_hh_se_arr = numpy.array(mng_hh_se)
        mng_hh_se_arr = mng_hh_se_arr[mng_hh_se_arr > 0]
        mng_hh_se_arr = mng_hh_se_arr[numpy.isfinite(mng_hh_se_arr)]
        mng_hh_se_mean = numpy.mean(mng_hh_se_arr)
        mng_hh_se_median = numpy.median(mng_hh_se_arr)

        mng_hv_arr = numpy.array(mng_hv)
        mng_hv_arr = mng_hv_arr[mng_hv_arr < 0]
        mng_hv_arr = mng_hv_arr[numpy.isfinite(mng_hv_arr)]
        mng_hv_mean = numpy.mean(mng_hv_arr)
        mng_hv_median = numpy.median(mng_hv_arr)

        mng_hv_se_arr = numpy.array(mng_hv_se)
        mng_hv_se_arr = mng_hv_se_arr[mng_hv_se_arr > 0]
        mng_hv_se_arr = mng_hv_se_arr[numpy.isfinite(mng_hv_se_arr)]
        mng_hv_se_mean = numpy.mean(mng_hv_se_arr)
        mng_hv_se_median = numpy.median(mng_hv_se_arr)

        nmng_hh_arr = numpy.array(nmng_hh)
        nmng_hh_arr = nmng_hh_arr[nmng_hh_arr < 0]
        nmng_hh_arr = nmng_hh_arr[numpy.isfinite(nmng_hh_arr)]
        nmng_hh_mean = numpy.mean(nmng_hh_arr)
        nmng_hh_median = numpy.median(nmng_hh_arr)

        nmng_hh_se_arr = numpy.array(nmng_hh_se)
        nmng_hh_se_arr = nmng_hh_se_arr[nmng_hh_se_arr > 0]
        nmng_hh_se_arr = nmng_hh_se_arr[numpy.isfinite(nmng_hh_se_arr)]
        nmng_hh_se_mean = numpy.mean(nmng_hh_se_arr)
        nmng_hh_se_median = numpy.median(nmng_hh_se_arr)

        nmng_hv_arr = numpy.array(nmng_hv)
        nmng_hv_arr = nmng_hv_arr[nmng_hv_arr < 0]
        nmng_hv_arr = nmng_hv_arr[numpy.isfinite(nmng_hv_arr)]
        nmng_hv_mean = numpy.mean(nmng_hv_arr)
        nmng_hv_median = numpy.median(nmng_hv_arr)

        nmng_hv_se_arr = numpy.array(nmng_hv_se)
        nmng_hv_se_arr = nmng_hv_se_arr[nmng_hv_se_arr > 0]
        nmng_hv_se_arr = nmng_hv_se_arr[numpy.isfinite(nmng_hv_se_arr)]
        nmng_hv_se_mean = numpy.mean(nmng_hv_se_arr)
        nmng_hv_se_median = numpy.median(nmng_hv_se_arr)

        for year in years:
            if abs(prj_out_thresholds[year]['mng_hh'] - mng_hh_median) > 200:
                prj_out_thresholds[year]['mng_hh'] = mng_hh_median
                prj_out_thresholds[year]['mng_hh_se'] = mng_hh_se_median

            if abs(prj_out_thresholds[year]['mng_hv'] - mng_hv_median) > 200:
                prj_out_thresholds[year]['mng_hv'] = mng_hv_median
                prj_out_thresholds[year]['mng_hv_se'] = mng_hv_se_median

            if abs(prj_out_thresholds[year]['nmng_hh'] - nmng_hh_median) > 200:
                prj_out_thresholds[year]['nmng_hh'] = nmng_hh_median
                prj_out_thresholds[year]['nmng_hh_se'] = nmng_hh_se_median

            if abs(prj_out_thresholds[year]['nmng_hv'] - nmng_hv_median) > 200:
                prj_out_thresholds[year]['nmng_hv'] = nmng_hv_median
                prj_out_thresholds[year]['nmng_hv_se'] = nmng_hv_se_median

        prj_out_thresholds['mng_hh_median'] = mng_hh_median
        prj_out_thresholds['mng_hh_se_median'] = mng_hh_se_median
        prj_out_thresholds['mng_hv_median'] = mng_hv_median
        prj_out_thresholds['mng_hv_se_median'] = mng_hv_se_median
        prj_out_thresholds['nmng_hh_median'] = nmng_hh_median
        prj_out_thresholds['nmng_hh_se_median'] = nmng_hh_se_median
        prj_out_thresholds['nmng_hv_median'] = nmng_hv_median
        prj_out_thresholds['nmng_hv_se_median'] = nmng_hv_se_median
        prj_out_thresholds['mng_hh_mean'] = mng_hh_mean
        prj_out_thresholds['mng_hh_se_mean'] = mng_hh_se_mean
        prj_out_thresholds['mng_hv_mean'] = mng_hv_mean
        prj_out_thresholds['mng_hv_se_mean'] = mng_hv_se_mean
        prj_out_thresholds['nmng_hh_mean'] = nmng_hh_mean
        prj_out_thresholds['nmng_hh_se_mean'] = nmng_hh_se_mean
        prj_out_thresholds['nmng_hv_mean'] = nmng_hv_mean
        prj_out_thresholds['nmng_hv_se_mean'] = nmng_hv_se_mean

        out_file = os.path.join(out_dir, "{}_fnl_thresholds.json".format(prj))
        writeDict2JSON(prj_out_thresholds, out_file)





prj_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_projects_luts.json"
#thres_base_dir = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010"

all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
years_l1 = ['1996']#, '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']
for l1_year in years_l1:
    base_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{}'.format(l1_year)
    out_dir = os.path.join(base_dir, "fnl_prj_thresholds")
    chng_years = all_years.copy()
    chng_years.remove(l1_year)
    calcFnlPrjThreholds(prj_lut_file, base_dir, out_dir, chng_years, l1_year)



