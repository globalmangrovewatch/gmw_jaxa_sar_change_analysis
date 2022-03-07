import rsgislib.vectorutils


vec_base_file = "../02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
vec_base_lyr = "gmw_change_site_bboxs_ids"

vec_join_file = "ls_wrs2_scns.geojson"
vec_join_lyr = "ls_wrs2_scns"

out_vec_file = "gmw_change_site_bboxs_ids_wrs2.geojson"
out_vec_lyr = "gmw_change_site_bboxs_ids_wrs2"

rsgislib.vectorutils.perform_spatial_join(vec_base_file, vec_base_lyr, vec_join_file, vec_join_lyr, out_vec_file, out_vec_lyr, out_format = 'GeoJSON', join_how = 'inner', join_op = 'within')