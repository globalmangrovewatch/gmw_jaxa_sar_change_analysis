import pandas
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


def get_data(tiles, base_dir, key_val):
    vals = list()
    for tile in tiles:
        input_file = os.path.join(base_dir, "GMW_{}_stats.json".format(tile))
        if not os.path.exists(input_file):
            raise Exception("Input file was not available: {}".format(input_file))
        data = readJSON2Dict(input_file)
        vals.append(data[key_val])
    return vals


def run_summarise_stats(tile_lut_file, in_data_dir, base_year_data_dir, base_year, before_years, after_years, output_file):

    tile_lut_dict = readJSON2Dict(tile_lut_file)
    tile_lut_dict.pop("N13E045")
    tile_idx_lst = tile_lut_dict.keys()

    base_dir = os.path.join(in_data_dir, base_year_data_dir)
    mng_ext_base = get_data(tile_idx_lst, base_dir, base_year)

    if len(before_years) > 0:
        out_mng_before_data = dict()
        out_mng_before_data["{} Extent".format(base_year)] = mng_ext_base
        for year in before_years:
            base_dir = os.path.join(in_data_dir, "gmw_{}_{}_chngs_stats".format(base_year, year))
            out_mng_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_mng')

        out_nmng_before_data = dict()
        out_nmng_before_data["{} Extent".format(base_year)] = mng_ext_base
        for year in before_years:
            base_dir = os.path.join(in_data_dir, "gmw_{}_{}_chngs_stats".format(base_year, year))
            out_nmng_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_nmng')

        df_mng_before_data = pandas.DataFrame(out_mng_before_data, index=tile_idx_lst)
        df_nmng_before_data = pandas.DataFrame(out_nmng_before_data, index=tile_idx_lst)

    if len(after_years) > 0:
        out_mng_after_data = dict()
        out_mng_after_data["{} Extent".format(base_year)] = mng_ext_base
        for year in after_years:
            base_dir = os.path.join(in_data_dir, "gmw_{}_{}_chngs_stats".format(base_year, year))
            out_mng_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_mng')

        out_nmng_after_data = dict()
        out_nmng_after_data["{} Extent".format(base_year)] = mng_ext_base
        for year in after_years:
            base_dir = os.path.join(in_data_dir, "gmw_{}_{}_chngs_stats".format(base_year, year))
            out_nmng_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_nmng')


        df_mng_after_data = pandas.DataFrame(out_mng_after_data, index=tile_idx_lst)
        df_nmng_after_data = pandas.DataFrame(out_nmng_after_data, index=tile_idx_lst)


    # Create a Pandas Excel writer using XlsxWriter as the engine.
    xls_writer = pandas.ExcelWriter(output_file, engine='xlsxwriter')

    if len(before_years) > 0:
        df_mng_before_data.to_excel(xls_writer, sheet_name='before_{}_mng_to_nmng'.format(base_year))
        df_nmng_before_data.to_excel(xls_writer, sheet_name='before_{}_nmng_to_mng'.format(base_year))

    if len(after_years) > 0:
        df_mng_after_data.to_excel(xls_writer, sheet_name='after_{}_mng_to_nmng'.format(base_year))
        df_nmng_after_data.to_excel(xls_writer, sheet_name='after_{}_nmng_to_mng'.format(base_year))

    xls_writer.save()





tile_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_tiles_luts.json"

all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
years_l1 = ['1996']#, '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']
for l1_year in years_l1:
    in_data_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{}'.format(l1_year)
    if l1_year == "2020":
        base_year_data_dir = "gmw_{}_2019_chngs_stats".format(l1_year)
    else:
        base_year_data_dir = "gmw_{}_2020_chngs_stats".format(l1_year)
    output_file = 'gmw_tile_raw_chng_feat_stats_304_base{}.xlsx'.format(l1_year)

    before_years = []
    after_years = []
    found_year = False
    for year in all_years:
        if year == l1_year:
            found_year = True
        else:
            if found_year:
                after_years.append(year)
            else:
                before_years.append(year)

    run_summarise_stats(tile_lut_file, in_data_dir, base_year_data_dir, l1_year, before_years, after_years, output_file)