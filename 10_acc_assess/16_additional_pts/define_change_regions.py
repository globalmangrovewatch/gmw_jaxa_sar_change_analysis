import os
import pprint

import rsgislib.vectorattrs
import rsgislib.tools.utils
import rsgislib.imagecalc
import rsgislib.rastergis
import rsgislib.vectorutils.createrasters

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

ls_sites_lut_file = "../13_create_imgs_lut/ls_imgs_lut_edit.json"
ls_sites_lut = rsgislib.tools.utils.read_json_to_dict(ls_sites_lut_file)

tmp_dir = "tmp"
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

out_dir = "../00_data/05_chng_rgns_max_time"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for roi_id in roi_ids:
    site_chng_dir = f"../00_data/02_site_chng_maps/site_{roi_id}"
    site_ls_years = ls_sites_lut["{}".format(roi_id)]
    site_ls_years.sort()
    #print(site_ls_years)
    base_year = site_ls_years[0]
    chng_year = site_ls_years[-1]
    print(f"site {roi_id}: {base_year} -- {chng_year}")

    ref_chng_img = os.path.join(site_chng_dir, f"gmw_chng_site_{roi_id}_{base_year}_{chng_year}.kea")
    out_img = os.path.join(out_dir, f"site_{roi_id}_chng_pxls.kea")

    if sites_info[roi_id] is None:
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('ref_chng', ref_chng_img, 1))
        rsgislib.imagecalc.band_math(out_img, '(ref_chng==3)||(ref_chng==4):1?0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
    elif sites_info[roi_id] == "all":
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('ref_chng', ref_chng_img, 1))
        rsgislib.imagecalc.band_math(out_img, '1', 'KEA', rsgislib.TYPE_8UINT, band_defns)
    else:
        tmp_img = os.path.join(tmp_dir, f"site_{roi_id}_chng_rgns.kea")
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(vec_file="change_regions_polys.geojson", vec_lyr="change_regions_polys", input_img=ref_chng_img, output_img=tmp_img, gdalformat='KEA', burn_val=1, datatype=rsgislib.TYPE_8UINT)

        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('ref_chng', ref_chng_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('chng_rgn', tmp_img, 1))
        rsgislib.imagecalc.band_math(out_img, 'chng_rgn==1?1:(ref_chng==3)||(ref_chng==4)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)

    rsgislib.rastergis.pop_rat_img_stats(out_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)










