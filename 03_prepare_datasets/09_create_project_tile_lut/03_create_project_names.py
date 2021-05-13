import geopandas
import numpy
import rsgislib

rsgis_utils = rsgislib.RSGISPyUtils()

gp_df = geopandas.read_file('gmw_degree_tiles_mpop.geojson')

for row in range(gp_df.shape[0]):
    prj_name = "GMW-{}-{}".format(rsgis_utils.zero_pad_num_str(gp_df.iloc[row].prj_p1, 2, integerise=True),
                                  rsgis_utils.zero_pad_num_str(gp_df.iloc[row].prj_p2, 3, integerise=True))
    print(prj_name)
    gp_df.at[row, 'prj_name'] = prj_name

gp_df.to_file('gmw_degree_tiles_fnl.geojson', driver='GeoJSON')
