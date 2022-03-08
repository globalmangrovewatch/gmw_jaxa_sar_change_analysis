import random
import os

import rsgislib.classification
import rsgislib.tools.utils

ref_img_base_dir = "/home/pete/Development/globalmangrovewatch/gmw_jaxa_sar_change_analysis/10_acc_assess/00_data/02_site_chng_maps"

out_vec_dir = "acc_ref_pts"
if not os.path.exists(out_vec_dir):
    os.mkdir(out_vec_dir)

sites_lut_file = "../13_create_imgs_lut/ls_imgs_lut_edit.json"
sites_lut = rsgislib.tools.utils.read_json_to_dict(sites_lut_file)

for site in sites_lut:
    print(site)
    site_years = sites_lut[site]
    site_years.sort()
    #print(site_years)
    base_year = random.choice(site_years[:-1])
    base_year_idx = site_years.index(base_year)+1
    #print(base_year)
    #print(base_year_idx)
    chng_year = random.choice(site_years[base_year_idx:])

    print(f"\t{base_year} -- {chng_year}")
    site_dir = os.path.join(ref_img_base_dir, "site_{}".format(site))

    ref_img_file = f"gmw_chng_site_{site}_{base_year}_{chng_year}.kea"

    ref_img_file_path = os.path.join(site_dir, ref_img_file)
    print(ref_img_file_path)

    acc_vec_file = os.path.join(out_vec_dir, f"gmw_chng_site_{site}_{base_year}_{chng_year}_acc_pts.geojson")
    out_vec_lyr = f"gmw_chng_site_{site}_{base_year}_{chng_year}_acc_pts"

    rsgislib.classification.generate_random_accuracy_pts(ref_img_file_path, acc_vec_file, out_vec_lyr, "GeoJSON", "class_names", "chng_cls", "chng_ref", 500, 42, True)