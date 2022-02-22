import os

import tqdm

import rsgislib.vectorattrs
import rsgislib.imagecalc
import rsgislib.tools.utils

roi_vec = "../02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
roi_lyr = "gmw_change_site_bboxs_ids"

roi_ids = rsgislib.vectorattrs.read_vec_column(roi_vec, roi_lyr, "roi_id")

gmw_years = [1996, 2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]

class_info_dict = dict()
class_info_dict[1] = {
    "classname": "Mangroves",
    "red": 0,
    "green": 255,
    "blue": 0,
}
class_info_dict[2] = {
    "classname": "Not Mangroves",
    "red": 180,
    "green": 180,
    "blue": 180,
}
class_info_dict[3] = {
    "classname": "Mangroves > Not Mangroves",
    "red": 255,
    "green": 0,
    "blue": 0,
}
class_info_dict[4] = {
    "classname": "Not Mangroves > Mangroves",
    "red": 0,
    "green": 0,
    "blue": 255,
}

site_chng_pxls_counts = dict()

for roi_id in tqdm.tqdm(roi_ids):
    #print(f"site: {roi_id}")
    roi_dir = f"../00_data/02_site_chng_maps/site_{roi_id}"
    for base_year in gmw_years:
        #print(f"\tBase Year: {base_year}")
        for chng_year in gmw_years:
            #print(f"\t\tChange Year: {chng_year}")
            if base_year == chng_year:
                continue
            elif base_year < chng_year:
                chng_img = os.path.join(roi_dir, f"gmw_chng_site_{roi_id}_{base_year}_{chng_year}.kea")
                n_cls_pxls = rsgislib.imagecalc.count_pxls_of_val(chng_img, vals=[1,2,3,4])
                tot_cls_pxls = sum(n_cls_pxls)
                prop_cls_pxls = list()
                for val in n_cls_pxls:
                    prop_cls_pxls.append((val/tot_cls_pxls)*100)
                cls_key = f"{roi_id}_b{base_year}_c{chng_year}"
                site_chng_pxls_counts[cls_key] = dict()
                site_chng_pxls_counts[cls_key]["total"] = tot_cls_pxls
                site_chng_pxls_counts[cls_key]["cls_pxls"] = n_cls_pxls
                site_chng_pxls_counts[cls_key]["cls_prop"] = prop_cls_pxls

rsgislib.tools.utils.write_dict_to_json(site_chng_pxls_counts, "site_chng_pxl_counts.json")
