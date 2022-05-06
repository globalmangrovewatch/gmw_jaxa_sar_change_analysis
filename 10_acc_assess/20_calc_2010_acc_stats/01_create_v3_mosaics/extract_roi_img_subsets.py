import rsgislib
import rsgislib.imageutils


input_img = "/Users/pete/Development/globalmangrovewatch/gmw_jaxa_sar_change_analysis/10_acc_assess/20_calc_2010_acc_stats/01_create_v3_mosaics/gmw_2010_extent_v314.vrt"
vec_file = "../00_datasets/roi_centre_bboxs_roi_ids.geojson"
vec_lyr = "roi_centre_bboxs_roi_ids"
out_img_base = "../00_datasets/roi_v314_imgs/gmw_acc_roi_"


rsgislib.imageutils.subset_to_geoms_bbox(input_img, vec_file, vec_lyr, "roi_id", out_img_base, "KEA", rsgislib.TYPE_8UINT, "kea")



