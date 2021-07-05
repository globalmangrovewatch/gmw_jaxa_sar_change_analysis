import tqdm
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

def writeDict2JSON(data_dict, out_file):
    """
    Write some data to a JSON file. The data would commonly be structured as a dict but could also be a list.

    :param data_dict: The dict (or list) to be written to the output JSON file.
    :param out_file: The file path to the output file.

    """
    import json
    with open(out_file, 'w') as fp:
        json.dump(data_dict, fp, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


def merge_tile_stats(input_files, output_file):
    out_stats = dict()
    out_stats['gmw_pxls'] = 0
    out_stats['pochng_pxls'] = 0
    out_stats['gmw_pxls_gt'] = list()
    out_stats['pochng_pxls_gt'] = list()
    out_stats['thresholds_gt'] = list()
    out_stats['gmw_pxls_lt'] = list()
    out_stats['pochng_pxls_lt'] = list()
    out_stats['thresholds_lt'] = list()

    gt_first = True
    lt_first = True
    mng_first = True
    nmng_first = True
    for input_file in tqdm.tqdm(input_files):
        some_data = False
        #print(input_file)
        stats_data = readJSON2Dict(input_file)
        #print("\t{}".format(stats_data['gmw_pxls']))

        if stats_data['gmw_pxls'] > 0:
            out_stats['gmw_pxls'] += stats_data['gmw_pxls']
            some_data = True
            if mng_first:
                out_stats['gmw_pxls_gt'] = stats_data['gmw_pxls_gt']
                out_stats['gmw_pxls_lt'] = stats_data['gmw_pxls_lt']
                mng_first = False
            else:
                if len(out_stats['gmw_pxls_gt']) != len(stats_data['gmw_pxls_gt']):
                    print(stats_data['gmw_pxls_gt'])
                    raise Exception("Number of mangrove bins GT are not equal.")
                if len(out_stats['gmw_pxls_lt']) != len(stats_data['gmw_pxls_lt']):
                    print(stats_data['gmw_pxls_lt'])
                    raise Exception("Number of mangrove bins LT are not equal.")
                for i in range(len(out_stats['gmw_pxls_gt'])):
                    out_stats['gmw_pxls_gt'][i] += stats_data['gmw_pxls_gt'][i]
                for i in range(len(out_stats['gmw_pxls_lt'])):
                    out_stats['gmw_pxls_lt'][i] += stats_data['gmw_pxls_lt'][i]


        if stats_data['pochng_pxls'] > 0:
            out_stats['pochng_pxls'] += stats_data['pochng_pxls']
            some_data = True
            if nmng_first:
                out_stats['pochng_pxls_gt'] = stats_data['pochng_pxls_gt']
                out_stats['pochng_pxls_lt'] = stats_data['pochng_pxls_lt']
                nmng_first = False
            else:
                if len(out_stats['pochng_pxls_gt']) != len(stats_data['pochng_pxls_gt']):
                    print(stats_data['pochng_pxls_gt'])
                    raise Exception("Number of non-mangrove bins GT are not equal.")
                if len(out_stats['pochng_pxls_lt']) != len(stats_data['pochng_pxls_lt']):
                    print(stats_data['pochng_pxls_lt'])
                    raise Exception("Number of non-mangrove bins LT are not equal.")
                for i in range(len(out_stats['pochng_pxls_gt'])):
                    out_stats['pochng_pxls_gt'][i] += stats_data['pochng_pxls_gt'][i]
                for i in range(len(out_stats['pochng_pxls_lt'])):
                    out_stats['pochng_pxls_lt'][i] += stats_data['pochng_pxls_lt'][i]

        if some_data and gt_first:
            out_stats['thresholds_gt'] = stats_data['thresholds_gt']
            gt_first = False
        elif some_data:
            if len(out_stats['thresholds_gt']) != len(stats_data['thresholds_gt']):
                print(stats_data)
                raise Exception("Number of thresholds within the GT parameter are not equal.")

        if some_data and lt_first:
            out_stats['thresholds_lt'] = stats_data['thresholds_lt']
            lt_first = False
        elif some_data:
            if len(out_stats['thresholds_lt']) != len(stats_data['thresholds_lt']):
                print(stats_data)
                raise Exception("Number of thresholds within the LT parameter are not equal.")




    writeDict2JSON(out_stats, output_file)


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


# Merge Global Stats
import glob
input_files = glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_hv_test_thresholds/GMW_*.json')
merge_tile_stats(input_files, '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/global_hv_stats.json')

import glob
input_files = glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_hh_test_thresholds/GMW_*.json')
merge_tile_stats(input_files, '/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/global_hh_stats.json')


prj_lut_file = '../../../03_prepare_datasets/09_create_project_tile_lut/gmw_projects_luts.json'
prj_lut = readJSON2Dict(prj_lut_file)

for prj in prj_lut:
    print(prj_lut[prj])
    data_files = list()
    for tile in prj_lut[prj]:
        tmp_file = findFileNone('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_hv_test_thresholds/', '*{}*.json'.format(tile))
        if tmp_file is not None:
            data_files.append(tmp_file)

    if len(data_files) > 0:
        out_file = os.path.join('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_prj_info_hv', '{}_stats.json'.format(prj))
        merge_tile_stats(data_files, out_file)


for prj in prj_lut:
    print(prj_lut[prj])
    data_files = list()
    for tile in prj_lut[prj]:
        tmp_file = findFileNone('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_hh_test_thresholds/', '*{}*.json'.format(tile))
        if tmp_file is not None:
            data_files.append(tmp_file)

    if len(data_files) > 0:
        out_file = os.path.join('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_prj_info_hh', '{}_stats.json'.format(prj))
        merge_tile_stats(data_files, out_file)


