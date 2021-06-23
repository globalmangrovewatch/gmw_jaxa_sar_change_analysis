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

mng_hh_thres = dict()
mng_hv_thres = dict()
nmng_hh_thres = dict()
nmng_hv_thres = dict()

for prj in prj_idx_lst:
    mng_hh_thres[prj] = list()
    mng_hv_thres[prj] = list()
    nmng_hh_thres[prj] = list()
    nmng_hv_thres[prj] = list()

years = ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']

for prj in prj_idx_lst:
    print(prj)
    for year in years:
        thres_lut_dir = '/Users/pete/Temp/gmw_v3_analysis/calc_v3_chng_thresholds/c_thresholds/gmw_2010_{}_prj_thres'.format(year)

        thres_file = findFileNone(thres_lut_dir, '{}*.json'.format(prj))

        if thres_file is not None:
            thres_dict = readJSON2Dict(thres_file)
            if 'mng_hh' in thres_dict:
                mng_hh_thres[prj].append(thres_dict['mng_hh'])
            else:
                mng_hh_thres[prj].append(0)

            if 'mng_hv' in thres_dict:
                mng_hv_thres[prj].append(thres_dict['mng_hv'])
            else:
                mng_hv_thres[prj].append(0)

            if 'nmng_hh' in thres_dict:
                nmng_hh_thres[prj].append(thres_dict['nmng_hh'])
            else:
                nmng_hh_thres[prj].append(0)

            if 'nmng_hv' in thres_dict:
                nmng_hv_thres[prj].append(thres_dict['nmng_hv'])
            else:
                nmng_hv_thres[prj].append(0)
        else:
            mng_hh_thres[prj].append(0)
            mng_hv_thres[prj].append(0)
            nmng_hh_thres[prj].append(0)
            nmng_hv_thres[prj].append(0)

col_names = get_year_named(years, 'mng_hh')
df_mng_hh_thres = pandas.DataFrame.from_dict(mng_hh_thres, orient='index', columns=col_names)
df_mng_hh_thres['prj_name'] = prj_idx_lst
for year in col_names:
    df_mng_hh_thres.loc[(df_mng_hh_thres[year] == 0), year] = None
    df_mng_hh_thres[year] = df_mng_hh_thres[year] / 100.0

col_names = get_year_named(years, 'mng_hv')
df_mng_hv_thres = pandas.DataFrame.from_dict(mng_hv_thres, orient='index', columns=col_names)
df_mng_hv_thres['prj_name'] = prj_idx_lst
for year in col_names:
    df_mng_hv_thres.loc[(df_mng_hv_thres[year] == 0), year] = None
    df_mng_hv_thres[year] = df_mng_hv_thres[year] / 100.0

col_names = get_year_named(years, 'nmng_hh')
df_nmng_hh_thres = pandas.DataFrame.from_dict(nmng_hh_thres, orient='index', columns=col_names)
df_nmng_hh_thres['prj_name'] = prj_idx_lst
for year in col_names:
    df_nmng_hh_thres.loc[(df_nmng_hh_thres[year] == 0), year] = None
    df_nmng_hh_thres[year] = df_nmng_hh_thres[year] / 100.0

col_names = get_year_named(years, 'nmng_hv')
df_nmng_hv_thres = pandas.DataFrame.from_dict(nmng_hv_thres, orient='index', columns=col_names)
df_nmng_hv_thres['prj_name'] = prj_idx_lst
for year in col_names:
    df_nmng_hv_thres.loc[(df_nmng_hv_thres[year] == 0), year] = None
    df_nmng_hv_thres[year] = df_nmng_hv_thres[year] / 100.0


# Create a Pandas Excel writer using XlsxWriter as the engine.
xls_writer = pandas.ExcelWriter('gmw_chng_thresholds.xlsx', engine='xlsxwriter')

df_mng_hh_thres.to_excel(xls_writer, sheet_name='mng_hh')
df_mng_hv_thres.to_excel(xls_writer, sheet_name='mng_hv')
df_nmng_hh_thres.to_excel(xls_writer, sheet_name='nmng_hh')
df_nmng_hv_thres.to_excel(xls_writer, sheet_name='nmng_hv')

xls_writer.save()


gdf_tiles = geopandas.read_file('../../../03_prepare_datasets/09_create_project_tile_lut/gmw_degree_tiles_fnl.geojson')

gdf_tiles_rslt = pandas.merge(gdf_tiles, df_mng_hh_thres, on="prj_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_mng_hv_thres, on="prj_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_nmng_hh_thres, on="prj_name")
gdf_tiles_rslt = pandas.merge(gdf_tiles_rslt, df_nmng_hv_thres, on="prj_name")

#gdf_tiles.join(df_mng_hh_thres, on='prj_name', rsuffix='mnghh')

gdf_tiles_rslt.to_file('gmw_tiles_prj_thres.gpkg', layer='gmw_prjs_thresholds', driver='GPKG')
