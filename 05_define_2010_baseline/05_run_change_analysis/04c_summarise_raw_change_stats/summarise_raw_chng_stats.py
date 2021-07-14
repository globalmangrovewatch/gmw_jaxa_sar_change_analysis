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


in_data_dir = "/Users/pete/Temp/gmw_v3_analysis/v3_2010_refine_chng_thresholds/outputs/gmw_2010_2010_chngs_stats"

#in_data_dir = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data"

mng_ext_2010 = get_data(tile_idx_lst, in_data_dir, '2010')
mng_to_nmng = get_data(tile_idx_lst, in_data_dir, 'chng_mng')
nmng_to_mng = get_data(tile_idx_lst, in_data_dir, 'chng_nmng')

out_data = dict()
out_data['2010 Extent'] = mng_ext_2010
out_data['mng to nmng'] = mng_to_nmng
out_data['nmng to mng'] = nmng_to_mng

df_data = pandas.DataFrame(out_data, index=tile_idx_lst)


# Create a Pandas Excel writer using XlsxWriter as the engine.
xls_writer = pandas.ExcelWriter('gmw_tile_2010_raw_chng_feat_stats.xlsx', engine='xlsxwriter')

df_data.to_excel(xls_writer, sheet_name='2010_chng')

xls_writer.save()
