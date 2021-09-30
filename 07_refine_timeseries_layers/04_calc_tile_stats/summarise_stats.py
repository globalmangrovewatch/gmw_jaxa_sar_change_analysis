import pandas
import numpy
import os
import tqdm

def readJSON2Dict(input_file):
    """
    Read a JSON file. Will return a list or dict.

    :param input_file: input JSON file path.

    """
    import json
    with open(input_file) as f:
        data = json.load(f)
    return data


def summarise_stats(tile_lut_file, years, stats_files, output_file, sheet_name):
    tile_lut_dict = readJSON2Dict(tile_lut_file)
    tile_lut_dict.pop("N13E045")
    tile_idx_lst = list(tile_lut_dict.keys())
    tile_idx_lst.sort()
    tile_idx_arr = numpy.array(tile_idx_lst)

    stats_luts = dict()
    for year in years:
        stats_luts[year] = readJSON2Dict(stats_files[year])

    out_tile_stats = dict()
    for year in years:
        out_tile_stats[year] = list()
        for tile in tile_idx_lst:
            out_tile_stats[year].append(stats_luts[year][tile])

    df_tile_stats = pandas.DataFrame(out_tile_stats, index=tile_idx_arr)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    xls_writer = pandas.ExcelWriter(output_file, engine='xlsxwriter')
    df_tile_stats.to_excel(xls_writer, sheet_name=sheet_name)
    xls_writer.save()




lyrs = ['mjr']#, 'min', 'max']
tile_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_tiles_luts.json"
all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
for lyr in lyrs:
    stats_files = dict()
    for year in all_years:
        stats_files[year] = 'gmw_v3_mng_{}_ext_{}.json'.format(lyr, year)
    output_file = "gmw_v3_mng_{}_ext_tpflt_308.xlsx".format(lyr)
    sheet_name = "mng_{}_ext_308".format(lyr)
    summarise_stats(tile_lut_file, all_years, stats_files, output_file, sheet_name)

