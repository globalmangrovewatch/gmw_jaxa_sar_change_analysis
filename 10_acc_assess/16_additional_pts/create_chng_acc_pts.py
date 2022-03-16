import os
import math
import rsgislib

import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.vectorattrs
import rsgislib.tools.utils
import rsgislib.rastergis
import rsgislib.vectorutils.createvectors

roi_vec = "../02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
roi_lyr = "gmw_change_site_bboxs_ids"

roi_ids = rsgislib.vectorattrs.read_vec_column(roi_vec, roi_lyr, "roi_id")

ls_sites_lut_file = "../13_create_imgs_lut/ls_imgs_lut_edit.json"
ls_sites_lut = rsgislib.tools.utils.read_json_to_dict(ls_sites_lut_file)

chng_rgn_img_dir = "../00_data/05_chng_rgns_max_time"

chng_smpls_img_dir = "../00_data/06_chng_smpls_max_time"
if not os.path.exists(chng_smpls_img_dir):
    os.mkdir(chng_smpls_img_dir)

acc_pts_dir = "acc_chng_pts"
if not os.path.exists(acc_pts_dir):
    os.mkdir(acc_pts_dir)

for roi_id in roi_ids:
    site_ls_years = ls_sites_lut["{}".format(roi_id)]
    site_ls_years.sort()
    # print(site_ls_years)
    base_year = site_ls_years[0]
    chng_year = site_ls_years[-1]
    print(f"site {roi_id}: {base_year} -- {chng_year}")

    chng_ref_img = os.path.join(chng_rgn_img_dir, f"site_{roi_id}_chng_pxls.kea")
    chng_acc_smpls_img = os.path.join(chng_smpls_img_dir, f"site_{roi_id}_chng_acc_pxls.kea")

    chng_ref_pxls = rsgislib.imagecalc.count_pxls_of_val(input_img=chng_ref_img, vals=[1], img_band=1)[0]

    n_samples = 100
    if chng_ref_pxls < 100:
        n_samples = int(math.floor(chng_ref_pxls/2))

    rsgislib.imageutils.perform_random_pxl_sample_in_mask_low_pxl_count(input_img=chng_ref_img, output_img=chng_acc_smpls_img, gdalformat="KEA", mask_vals=1, n_samples=n_samples, rnd_seed=42)
    rsgislib.rastergis.pop_rat_img_stats(chng_acc_smpls_img, add_clr_tab=True, calc_pyramids=True, ignore_zero=True)

    chng_acc_smpls_vec = os.path.join(acc_pts_dir, f"site_{roi_id}_{base_year}_{chng_year}_chng_acc_pts.geojson")
    rsgislib.vectorutils.createvectors.vectorise_pxls_to_pts(chng_acc_smpls_img, img_band=1, img_msk_val=1, out_vec_file=chng_acc_smpls_vec, out_vec_lyr= None, out_format='GeoJSON', del_exist_vec=True)