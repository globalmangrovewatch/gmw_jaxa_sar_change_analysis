import pandas
import geopandas
import glob
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

tiles_lut_file = "../../../03_prepare_datasets/09_create_project_tile_lut/gmw_tiles_luts.json"
tiles_lut_dict = readJSON2Dict(tiles_lut_file)
tiles_idx_lst = tiles_lut_dict.keys()


tile_hh_mean = dict()
tile_hh_stdev = dict()
tile_hh_n = dict()
tile_hh_sum = dict()

tile_hv_mean = dict()
tile_hv_stdev = dict()
tile_hv_n = dict()
tile_hv_sum = dict()

for tile in tiles_idx_lst:
    tile_hh_mean[tile] = list()
    tile_hh_stdev[tile] = list()
    tile_hh_n[tile] = list()
    tile_hh_sum[tile] = list()

    tile_hv_mean[tile] = list()
    tile_hv_stdev[tile] = list()
    tile_hv_n[tile] = list()
    tile_hv_sum[tile] = list()

years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']


for tile in tiles_idx_lst:
    for year in years:
        tile_lut_dir = '/Users/pete/Temp/gmw_v3_analysis/jaxa_sar_timeseries_analysis/jaxa_tile_stats/sar_tile_{}_stats'.format(year)

        tile_stats_file = os.path.join(tile_lut_dir, "{0}_{1}_db_{1}_stats.json".format(tile, year))
        if os.path.exists(tile_stats_file):
            tile_stat_dict = readJSON2Dict(tile_stats_file)

            if 'hh_mean' in tile_stat_dict:
                tile_hh_mean[tile].append(tile_stat_dict['hh_mean'])
            else:
                tile_hh_mean[tile].append(0)
            if 'hh_stddev' in tile_stat_dict:
                tile_hh_stdev[tile].append(tile_stat_dict['hh_stddev'])
            else:
                tile_hh_stdev[tile].append(0)
            if 'hh_n' in tile_stat_dict:
                tile_hh_n[tile].append(tile_stat_dict['hh_n'])
            else:
                tile_hh_n[tile].append(0)
            if 'hh_sum' in tile_stat_dict:
                tile_hh_sum[tile].append(tile_stat_dict['hh_sum'])
            else:
                tile_hh_sum[tile].append(0)
                
            if 'hv_mean' in tile_stat_dict:
                tile_hv_mean[tile].append(tile_stat_dict['hv_mean'])
            else:
                tile_hv_mean[tile].append(0)
            if 'hv_stddev' in tile_stat_dict:
                tile_hv_stdev[tile].append(tile_stat_dict['hv_stddev'])
            else:
                tile_hv_stdev[tile].append(0)
            if 'hv_n' in tile_stat_dict:
                tile_hv_n[tile].append(tile_stat_dict['hv_n'])
            else:
                tile_hv_n[tile].append(0)
            if 'hv_sum' in tile_stat_dict:
                tile_hv_sum[tile].append(tile_stat_dict['hv_sum'])
            else:
                tile_hv_sum[tile].append(0)

        else:
            tile_hh_mean[tile].append(0)
            tile_hh_stdev[tile].append(0)
            tile_hh_n[tile].append(0)
            tile_hh_sum[tile].append(0)

            tile_hv_mean[tile].append(0)
            tile_hv_stdev[tile].append(0)
            tile_hv_n[tile].append(0)
            tile_hv_sum[tile].append(0)



col_names = get_year_named(years, 'hh_mean')
df_hh_mean = pandas.DataFrame.from_dict(tile_hh_mean, orient='index', columns=col_names)
df_hh_mean['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hh_mean.loc[(df_hh_mean[year] == 0), year] = None
    df_hh_mean[year] = df_hh_mean[year] / 100.0

col_names = get_year_named(years, 'hh_stdev')
df_hh_stdev = pandas.DataFrame.from_dict(tile_hh_stdev, orient='index', columns=col_names)
df_hh_stdev['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hh_stdev.loc[(df_hh_stdev[year] == 0), year] = None
    df_hh_stdev[year] = df_hh_stdev[year] / 100.0

col_names = get_year_named(years, 'hh_n')
df_hh_n = pandas.DataFrame.from_dict(tile_hh_n, orient='index', columns=col_names)
df_hh_n['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hh_n.loc[(df_hh_n[year] == 0), year] = None
    df_hh_n[year] = df_hh_n[year] / 100.0
    
col_names = get_year_named(years, 'hh_sum')
df_hh_sum = pandas.DataFrame.from_dict(tile_hh_sum, orient='index', columns=col_names)
df_hh_sum['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hh_sum.loc[(df_hh_sum[year] == 0), year] = None
    df_hh_sum[year] = df_hh_sum[year] / 100.0

col_names = get_year_named(years, 'hv_mean')
df_hv_mean = pandas.DataFrame.from_dict(tile_hv_mean, orient='index', columns=col_names)
df_hv_mean['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hv_mean.loc[(df_hv_mean[year] == 0), year] = None
    df_hv_mean[year] = df_hv_mean[year] / 100.0

col_names = get_year_named(years, 'hv_stdev')
df_hv_stdev = pandas.DataFrame.from_dict(tile_hv_stdev, orient='index', columns=col_names)
df_hv_stdev['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hv_stdev.loc[(df_hv_stdev[year] == 0), year] = None
    df_hv_stdev[year] = df_hv_stdev[year] / 100.0

col_names = get_year_named(years, 'hv_n')
df_hv_n = pandas.DataFrame.from_dict(tile_hv_n, orient='index', columns=col_names)
df_hv_n['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hv_n.loc[(df_hv_n[year] == 0), year] = None
    df_hv_n[year] = df_hv_n[year] / 100.0

col_names = get_year_named(years, 'hv_sum')
df_hv_sum = pandas.DataFrame.from_dict(tile_hv_sum, orient='index', columns=col_names)
df_hv_sum['tile_name'] = tiles_idx_lst
for year in col_names:
    df_hv_sum.loc[(df_hv_sum[year] == 0), year] = None
    df_hv_sum[year] = df_hv_sum[year] / 100.0




gdf_tiles = geopandas.read_file('../../../03_prepare_datasets/09_create_project_tile_lut/gmw_degree_tiles_fnl.geojson')

gdf_tiles_rslt = pandas.merge(gdf_tiles, df_hh_mean, on="tile_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_hh_stdev, on="tile_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_hv_mean, on="tile_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_hv_stdev, on="tile_name")

gdf_tiles_rslt.to_file('gmw_tiles_jaxa_sar.gpkg', layer='gmw_tiles_jaxa_sar', driver='GPKG')



df_hh_mean = df_hh_mean.drop(columns="tile_name")
df_hh_stdev = df_hh_stdev.drop(columns="tile_name")
df_hh_n = df_hh_n.drop(columns="tile_name")
df_hh_sum = df_hh_sum.drop(columns="tile_name")
df_hv_mean = df_hv_mean.drop(columns="tile_name")
df_hv_stdev = df_hv_stdev.drop(columns="tile_name")
df_hv_n = df_hv_n.drop(columns="tile_name")
df_hv_sum = df_hv_sum.drop(columns="tile_name")

df_hh_mean.dropna(how='all', inplace=True)
df_hh_stdev.dropna(how='all', inplace=True)
df_hh_n.dropna(how='all', inplace=True)
df_hh_sum.dropna(how='all', inplace=True)
df_hv_mean.dropna(how='all', inplace=True)
df_hv_stdev.dropna(how='all', inplace=True)
df_hv_n.dropna(how='all', inplace=True)
df_hv_sum.dropna(how='all', inplace=True)


# Create a Pandas Excel writer using XlsxWriter as the engine.
xls_writer = pandas.ExcelWriter('jaxa_sar_tile_stats.xlsx', engine='xlsxwriter')

df_hh_mean.to_excel(xls_writer, sheet_name='hh_mean')
df_hh_stdev.to_excel(xls_writer, sheet_name='hh_stdev')
df_hh_n.to_excel(xls_writer, sheet_name='hh_n')
df_hh_sum.to_excel(xls_writer, sheet_name='hh_sum')

df_hv_mean.to_excel(xls_writer, sheet_name='hv_mean')
df_hv_stdev.to_excel(xls_writer, sheet_name='hv_stdev')
df_hv_n.to_excel(xls_writer, sheet_name='hv_n')
df_hv_sum.to_excel(xls_writer, sheet_name='hv_sum')

xls_writer.save()


