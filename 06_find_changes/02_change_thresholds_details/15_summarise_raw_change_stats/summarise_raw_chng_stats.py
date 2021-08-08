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


tile_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_tiles_luts.json"

tile_lut_dict = readJSON2Dict(tile_lut_file)
tile_lut_dict.pop("N13E045")
tile_idx_lst = tile_lut_dict.keys()


in_data_dir = "/Users/pete/Temp/gmw_v3_analysis/v3_raw_chng_feats/out_stats_update"

#in_data_dir = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data"

base_dir = os.path.join(in_data_dir, "gmw_2010_2020_chngs_stats")
mng_ext_2010 = get_data(tile_idx_lst, base_dir, '2010')
#print(mng_ext_2010)


before_years = ['1996', '2007', '2008', '2009']
after_years = ['2015', '2016', '2017', '2018', '2019', '2020']

out_mng_before_data = dict()
out_mng_before_data["2010 Extent"] = mng_ext_2010
for year in before_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_mng_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_mng')

out_nmng_before_data = dict()
out_nmng_before_data["2010 Extent"] = mng_ext_2010
for year in before_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_nmng_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_nmng')

"""
out_mng_lower_before_data = dict()
out_mng_lower_before_data["2010 Extent"] = mng_ext_2010
for year in before_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_mng_lower_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_low_mng')

out_nmng_lower_before_data = dict()
out_nmng_lower_before_data["2010 Extent"] = mng_ext_2010
for year in before_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_nmng_lower_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_low_nmng')

out_mng_upper_before_data = dict()
out_mng_upper_before_data["2010 Extent"] = mng_ext_2010
for year in before_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_mng_upper_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_up_mng')

out_nmng_upper_before_data = dict()
out_nmng_upper_before_data["2010 Extent"] = mng_ext_2010
for year in before_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_nmng_upper_before_data[year] = get_data(tile_idx_lst, base_dir, 'chng_up_nmng')
"""

df_mng_before_data = pandas.DataFrame(out_mng_before_data, index=tile_idx_lst)
df_nmng_before_data = pandas.DataFrame(out_nmng_before_data, index=tile_idx_lst)
"""
df_mng_lower_before_data = pandas.DataFrame(out_mng_lower_before_data, index=tile_idx_lst)
df_nmng_lower_before_data = pandas.DataFrame(out_nmng_lower_before_data, index=tile_idx_lst)

df_mng_upper_before_data = pandas.DataFrame(out_mng_upper_before_data, index=tile_idx_lst)
df_nmng_upper_before_data = pandas.DataFrame(out_nmng_upper_before_data, index=tile_idx_lst)
"""



out_mng_after_data = dict()
out_mng_after_data["2010 Extent"] = mng_ext_2010
for year in after_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_mng_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_mng')

out_nmng_after_data = dict()
out_nmng_after_data["2010 Extent"] = mng_ext_2010
for year in after_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_nmng_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_nmng')
"""
out_mng_lower_after_data = dict()
out_mng_lower_after_data["2010 Extent"] = mng_ext_2010
for year in after_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_mng_lower_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_low_mng')

out_nmng_lower_after_data = dict()
out_nmng_lower_after_data["2010 Extent"] = mng_ext_2010
for year in after_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_nmng_lower_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_low_nmng')

out_mng_upper_after_data = dict()
out_mng_upper_after_data["2010 Extent"] = mng_ext_2010
for year in after_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_mng_upper_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_up_mng')

out_nmng_upper_after_data = dict()
out_nmng_upper_after_data["2010 Extent"] = mng_ext_2010
for year in after_years:
    base_dir = os.path.join(in_data_dir, "gmw_2010_{}_chngs_stats".format(year))
    out_nmng_upper_after_data[year] = get_data(tile_idx_lst, base_dir, 'chng_up_nmng')
"""

df_mng_after_data = pandas.DataFrame(out_mng_after_data, index=tile_idx_lst)
df_nmng_after_data = pandas.DataFrame(out_nmng_after_data, index=tile_idx_lst)

"""
df_mng_lower_after_data = pandas.DataFrame(out_mng_lower_after_data, index=tile_idx_lst)
df_nmng_lower_after_data = pandas.DataFrame(out_nmng_lower_after_data, index=tile_idx_lst)

df_mng_upper_after_data = pandas.DataFrame(out_mng_upper_after_data, index=tile_idx_lst)
df_nmng_upper_after_data = pandas.DataFrame(out_nmng_upper_after_data, index=tile_idx_lst)
"""



# Create a Pandas Excel writer using XlsxWriter as the engine.
xls_writer = pandas.ExcelWriter('gmw_tile_raw_chng_feat_stats_updated.xlsx', engine='xlsxwriter')

df_mng_before_data.to_excel(xls_writer, sheet_name='before_2010_mng_to_nmng')
df_nmng_before_data.to_excel(xls_writer, sheet_name='before_2010_nmng_to_mng')

df_mng_after_data.to_excel(xls_writer, sheet_name='after_2010_mng_to_nmng')
df_nmng_after_data.to_excel(xls_writer, sheet_name='after_2010_nmng_to_mng')
"""
df_mng_lower_before_data.to_excel(xls_writer, sheet_name='before_low_2010_mng_to_nmng')
df_nmng_lower_before_data.to_excel(xls_writer, sheet_name='before_low_2010_nmng_to_mng')

df_mng_lower_after_data.to_excel(xls_writer, sheet_name='after_low_2010_mng_to_nmng')
df_nmng_lower_after_data.to_excel(xls_writer, sheet_name='after_low_2010_nmng_to_mng')

df_mng_upper_before_data.to_excel(xls_writer, sheet_name='before_up_2010_mng_to_nmng')
df_nmng_upper_before_data.to_excel(xls_writer, sheet_name='before_up_2010_nmng_to_mng')

df_mng_upper_after_data.to_excel(xls_writer, sheet_name='after_up_2010_mng_to_nmng')
df_nmng_upper_after_data.to_excel(xls_writer, sheet_name='after_up_2010_nmng_to_mng')
"""
xls_writer.save()
