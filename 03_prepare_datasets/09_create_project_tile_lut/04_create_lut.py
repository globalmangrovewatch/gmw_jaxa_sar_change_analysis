import geopandas
import rsgislib

rsgis_utils = rsgislib.RSGISPyUtils()

gp_df = geopandas.read_file('gmw_degree_tiles_fnl.geojson')

prj_lut = dict()
tile_lut = dict()

for row in range(gp_df.shape[0]):
    prj_name = gp_df.iloc[row].prj_name
    tile = gp_df.iloc[row].tile_name

    if prj_name not in prj_lut:
        prj_lut[prj_name] = list()

    if tile not in prj_lut[prj_name]:
        prj_lut[prj_name].append(tile)

    if tile not in tile_lut:
        tile_lut[tile] = prj_name


rsgis_utils.writeDict2JSON(prj_lut, 'gmw_projects_luts.json')
rsgis_utils.writeDict2JSON(tile_lut, 'gmw_tiles_luts.json')


