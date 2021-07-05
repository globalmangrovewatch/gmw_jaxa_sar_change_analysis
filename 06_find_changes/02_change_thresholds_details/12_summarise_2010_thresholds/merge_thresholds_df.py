import os.path

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


def summarise_thresholds(input_files, rgn_name, output_file):
    names = list()
    mng_thresholds = list()
    nmng_thresholds = list()
    n_mng_pxls = list()
    n_nmng_pxls = list()
    for input_file in input_files:
        print(input_file)
        name = os.path.splitext(os.path.basename(input_file))[0].split('_')[0]
        thres_data = readJSON2Dict(input_file)

        names.append(name)
        mng_thresholds.append(thres_data['mangrove'])
        nmng_thresholds.append(thres_data['not-mangrove'])
        n_mng_pxls.append(thres_data['n_mangrove_pxls'])
        n_nmng_pxls.append(thres_data['n_not-mangrove_pxls'])

    data_dict = dict()
    data_dict[rgn_name] = names
    data_dict['mng_thresholds'] = mng_thresholds
    data_dict['nmng_thresholds'] = nmng_thresholds
    data_dict['n_mng_pxls'] = n_mng_pxls
    data_dict['n_nmng_pxls'] = n_nmng_pxls
    df = pandas.DataFrame.from_dict(data_dict, orient='columns')

    df.loc[(df['mng_thresholds'] == 0), 'mng_thresholds'] = None
    df.loc[(df['nmng_thresholds'] == 0), 'nmng_thresholds'] = None
    df.loc[(df['n_mng_pxls'] == 0), 'n_mng_pxls'] = None
    df.loc[(df['n_nmng_pxls'] == 0), 'n_nmng_pxls'] = None

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    xls_writer = pandas.ExcelWriter(output_file, engine='xlsxwriter')
    df.to_excel(xls_writer, sheet_name='ref_thresholds')
    xls_writer.save()

import glob

summarise_thresholds(glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_hv_tile_thresholds/*.json'), 'tiles', 'gmw_2010_hv_ref_tile_thresholds.xlsx')
summarise_thresholds(glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_prj_info_hv_thresholds/*.json'), 'projects', 'gmw_2010_hv_ref_projects_thresholds.xlsx')


summarise_thresholds(glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_2010_hh_tile_thresholds/*.json'), 'tiles', 'gmw_2010_hh_ref_tile_thresholds.xlsx')
summarise_thresholds(glob.glob('/Users/pete/Temp/gmw_v3_analysis/threshold_test_2010/outputs/gmw_prj_info_hh_thresholds/*.json'), 'projects', 'gmw_2010_hh_ref_projects_thresholds.xlsx')


