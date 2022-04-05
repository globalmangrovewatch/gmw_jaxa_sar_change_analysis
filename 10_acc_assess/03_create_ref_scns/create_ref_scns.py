import os

import rsgislib.imageutils.imagelut
import rsgislib.vectorgeoms
import rsgislib.vectorattrs
import rsgislib.tools.projection
import rsgislib.imagecalc
import rsgislib.rastergis

gmw_hab_lut = "/bigdata/globalmangrovewatch/gmw_habitat_mask/v9_20220222/gmw_hab_v9_raster_lut.gpkg"
gmw_hab_lyr = "hab_v9"

gmw_low_bscat_lut = "/bigdata/globalmangrovewatch/gmw_v3_low_backscatter_regions/gmw_low_bscat_lut.gpkg"
gmw_low_bscat_lyr = "gmw_v3_lbscat"

gmw_extent_lut = "/bigdata/globalmangrovewatch/gmw_v312_extent/gmw_v312_ext_raster_lut.gpkg"


gmw_years = ["1996", "2007", "2008", "2009", "2010", "2015", "2016", "2017", "2018", "2019", "2020"]
gmw_info = dict()
for year in gmw_years:
    gmw_info[year] = dict()
    gmw_info[year]["lut_lyr"] = f"gmw_extent_{year}"
    gmw_info[year]["out_dir"] = f"../00_data/01_site_maps/{year}"
    if not os.path.exists(gmw_info[year]["out_dir"]):
        os.mkdir(gmw_info[year]["out_dir"])


tmp_dir = "/bigdata/processing_tmp/gmw_tmp"

roi_vec = "../02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
roi_lyr = "gmw_change_site_bboxs_ids"

bboxs = rsgislib.vectorgeoms.get_geoms_as_bboxs(roi_vec, roi_lyr)
roi_ids = rsgislib.vectorattrs.read_vec_column(roi_vec, roi_lyr, "roi_id")

wkt_str = rsgislib.tools.projection.get_wkt_from_epsg_code(4326)

class_info_dict = dict()
class_info_dict[1] = {
    "classname": "Mangroves",
    "red": 0,
    "green": 255,
    "blue": 0,
}
class_info_dict[2] = {
    "classname": "Not Mangroves",
    "red": 0,
    "green": 0,
    "blue": 255,
}

for bbox, roi_id in zip(bboxs, roi_ids):
    print(bbox)

    ref_img = os.path.join(tmp_dir, "ref_img_{}.kea".format(roi_id))

    rsgislib.imageutils.create_blank_img_from_bbox(bbox, wkt_str, ref_img, out_img_res=0.000222222222222, out_img_pxl_val=0.0, out_img_n_bands=1, gdalformat="KEA", datatype=rsgislib.TYPE_8UINT, snap_to_grid=True)

    hab_img = rsgislib.imageutils.imagelut.get_raster_lyr(bbox, gmw_hab_lut, gmw_hab_lyr, tmp_dir)
    low_bscat_img = rsgislib.imageutils.imagelut.get_raster_lyr(bbox, gmw_low_bscat_lut, gmw_low_bscat_lyr, tmp_dir)
    for year in gmw_years:
        mng_img = rsgislib.imageutils.imagelut.get_raster_lyr(bbox, gmw_extent_lut, gmw_info[year]["lut_lyr"], tmp_dir)
        out_img = os.path.join(gmw_info[year]["out_dir"], f"gmw_{year}_v312_site_{roi_id}.kea")

        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('ref', ref_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('mng', mng_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hab', hab_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('lbscat', low_bscat_img, 1))
        rsgislib.imagecalc.band_math(out_img, '(mng == 1)?1:(hab==1) || (lbscat==1)?2:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.pop_rat_img_stats(out_img, True, True, True)
        rsgislib.rastergis.set_class_names_colours(out_img, "class_names", class_info_dict)

