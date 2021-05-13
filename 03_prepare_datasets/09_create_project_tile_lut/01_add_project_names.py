import geopandas
import numpy
import glob
import rsgislib

rsgis_utils = rsgislib.RSGISPyUtils()

gmw_v2_prj_lut_files = glob.glob('gmw_v2_project_tiles/*.txt')

gp_df = geopandas.read_file('gmw_degree_tiles.geojson')
gp_df['prj_name'] = numpy.empty((gp_df.shape[0]), dtype='U')
gp_df['prj_p1'] = numpy.zeros((gp_df.shape[0]), dtype=int)
gp_df['prj_p2'] = numpy.zeros((gp_df.shape[0]), dtype=int)

print(gp_df.info())

for proj_lut_file in gmw_v2_prj_lut_files:
    prj_name = rsgis_utils.get_file_basename(proj_lut_file).replace('_tiles', '')
    print(prj_name)
    prj_name_parts = prj_name.split('-')
    prj_p1 = int(prj_name_parts[1])
    prj_p2 = int(prj_name_parts[2])
    print("\t{} : {}".format(prj_p1, prj_p2))
    prj_tiles = rsgis_utils.readTextFile2List(proj_lut_file)
    for tile in prj_tiles:
        print("\t\t{}".format(tile))
        #gp_df[gp_df.tile_name == tile]['prj_name'] = prj_name
        gp_df['prj_name'].loc[gp_df['tile_name'] == tile] = prj_name
        gp_df['prj_p1'].loc[gp_df['tile_name'] == tile] = prj_p1
        gp_df['prj_p2'].loc[gp_df['tile_name'] == tile] = prj_p2

gp_df.to_file('gmw_degree_tiles_out.geojson', driver='GeoJSON')