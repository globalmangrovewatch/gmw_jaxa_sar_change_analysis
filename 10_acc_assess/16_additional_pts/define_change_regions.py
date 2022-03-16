import os

import rsgislib.vectorattrs

roi_vec = "../02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
roi_lyr = "gmw_change_site_bboxs_ids"

roi_ids = rsgislib.vectorattrs.read_vec_column(roi_vec, roi_lyr, "roi_id")

sites_info = dict()
sites_info[1] = "all"
sites_info[2] = "change_regions_polys.geojson"
sites_info[3] = "all"
sites_info[4] = "change_regions_polys.geojson"
sites_info[5] = None
sites_info[6] = "change_regions_polys.geojson"
sites_info[7] = "change_regions_polys.geojson"
sites_info[8] = "change_regions_polys.geojson"
sites_info[9] = None
sites_info[10] = "change_regions_polys.geojson"
sites_info[11] = None
sites_info[12] = "change_regions_polys.geojson"
sites_info[13] = "change_regions_polys.geojson"
sites_info[14] = "change_regions_polys.geojson"
sites_info[15] = "change_regions_polys.geojson"
sites_info[16] = "change_regions_polys.geojson"
sites_info[17] = "change_regions_polys.geojson"
sites_info[18] = None
sites_info[19] = "change_regions_polys.geojson"
sites_info[20] = "change_regions_polys.geojson"
sites_info[21] = "change_regions_polys.geojson"
sites_info[22] = "change_regions_polys.geojson"
sites_info[23] = "change_regions_polys.geojson"
sites_info[24] = "change_regions_polys.geojson"
sites_info[25] = "change_regions_polys.geojson"
sites_info[26] = None
sites_info[27] = None
sites_info[28] = "change_regions_polys.geojson"
sites_info[29] = "change_regions_polys.geojson"
sites_info[30] = "change_regions_polys.geojson"
sites_info[31] = "change_regions_polys.geojson"
sites_info[32] = None
sites_info[33] = None
sites_info[34] = "change_regions_polys.geojson"
sites_info[35] = "change_regions_polys.geojson"
sites_info[36] = "change_regions_polys.geojson"
sites_info[37] = "change_regions_polys.geojson"
sites_info[38] = "change_regions_polys.geojson"

tmp_dir = "tmp"
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

for roi_id in roi_ids:
    site_chng_dir = f"../00_data/02_site_chng_maps/site_{roi_id}"
    out_dir =  f"../00_data/02_site_chng_maps/site_{roi_id}"









