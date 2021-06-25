import pandas
import geopandas

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

mean_hh_vals = dict()
stdev_hh_vals = dict()
mean_hv_vals = dict()
stdev_hv_vals = dict()

for prj in prj_idx_lst:
    mean_hh_vals[prj] = list()
    stdev_hh_vals[prj] = list()
    mean_hv_vals[prj] = list()
    stdev_hv_vals[prj] = list()

years = ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']

for prj in prj_idx_lst:
    print(prj)
    for year in years:
        stats_lut_dir = '/Users/pete/Temp/gmw_v3_analysis/jaxa_sar_timeseries_analysis/gmw_core_prj_stats/gmw_core_{}_prj_sar_stats'.format(year)

        stats_file = findFileNone(stats_lut_dir, '{}*.json'.format(prj))

        if stats_file is not None:
            stats_dict = readJSON2Dict(stats_file)
            if 'hh_mean' in stats_dict:
                mean_hh_vals[prj].append(stats_dict['hh_mean'])
            else:
                mean_hh_vals[prj].append(0)

            if 'hh_stddev' in stats_dict:
                stdev_hh_vals[prj].append(stats_dict['hh_stddev'])
            else:
                stdev_hh_vals[prj].append(0)

            if 'hv_mean' in stats_dict:
                mean_hv_vals[prj].append(stats_dict['hv_mean'])
            else:
                mean_hv_vals[prj].append(0)

            if 'hv_stddev' in stats_dict:
                stdev_hv_vals[prj].append(stats_dict['hv_stddev'])
            else:
                stdev_hv_vals[prj].append(0)
        else:
            mean_hh_vals[prj].append(0)
            stdev_hh_vals[prj].append(0)
            mean_hv_vals[prj].append(0)
            stdev_hv_vals[prj].append(0)

col_names = get_year_named(years, 'hh_mean')
df_mean_hh_vals = pandas.DataFrame.from_dict(mean_hh_vals, orient='index', columns=col_names)
df_mean_hh_vals['prj_name'] = prj_idx_lst
for year in col_names:
    df_mean_hh_vals.loc[(df_mean_hh_vals[year] == 0), year] = None
    df_mean_hh_vals[year] = df_mean_hh_vals[year] / 100.0

col_names = get_year_named(years, 'hh_sd')
df_stdev_hh_vals = pandas.DataFrame.from_dict(stdev_hh_vals, orient='index', columns=col_names)
df_stdev_hh_vals['prj_name'] = prj_idx_lst
for year in col_names:
    df_stdev_hh_vals.loc[(df_stdev_hh_vals[year] == 0), year] = None
    df_stdev_hh_vals[year] = df_stdev_hh_vals[year] / 100.0

col_names = get_year_named(years, 'hv_mean')
df_mean_hv_vals = pandas.DataFrame.from_dict(mean_hv_vals, orient='index', columns=col_names)
df_mean_hv_vals['prj_name'] = prj_idx_lst
for year in col_names:
    df_mean_hv_vals.loc[(df_mean_hv_vals[year] == 0), year] = None
    df_mean_hv_vals[year] = df_mean_hv_vals[year] / 100.0

col_names = get_year_named(years, 'hv_sd')
df_stdev_hv_vals = pandas.DataFrame.from_dict(stdev_hv_vals, orient='index', columns=col_names)
df_stdev_hv_vals['prj_name'] = prj_idx_lst
for year in col_names:
    df_stdev_hv_vals.loc[(df_stdev_hv_vals[year] == 0), year] = None
    df_stdev_hv_vals[year] = df_stdev_hv_vals[year] / 100.0


gdf_tiles = geopandas.read_file('../../../03_prepare_datasets/09_create_project_tile_lut/gmw_degree_tiles_fnl.geojson')

gdf_tiles_rslt = pandas.merge(gdf_tiles, df_mean_hh_vals, on="prj_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_stdev_hh_vals, on="prj_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_mean_hv_vals, on="prj_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_stdev_hv_vals, on="prj_name")

gdf_tiles_rslt.to_file('gmw_prj_core_sar_stats.gpkg', layer='gmw_prj_core_sar_stats', driver='GPKG')


df_mean_hh_vals = df_mean_hh_vals.drop(columns="prj_name")
df_stdev_hh_vals = df_stdev_hh_vals.drop(columns="prj_name")
df_mean_hv_vals = df_mean_hv_vals.drop(columns="prj_name")
df_stdev_hv_vals = df_stdev_hv_vals.drop(columns="prj_name")

# Create a Pandas Excel writer using XlsxWriter as the engine.
xls_writer = pandas.ExcelWriter('gmw_prj_core_sar_stats.xlsx', engine='xlsxwriter')

df_mean_hh_vals.to_excel(xls_writer, sheet_name='hh_mean')
df_stdev_hh_vals.to_excel(xls_writer, sheet_name='hh_sd')
df_mean_hv_vals.to_excel(xls_writer, sheet_name='hv_mean')
df_stdev_hv_vals.to_excel(xls_writer, sheet_name='hv_sd')

xls_writer.save()

