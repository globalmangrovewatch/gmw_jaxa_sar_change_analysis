import os

import rsgislib.vectorattrs
import rsgislib.imagecalc
import rsgislib.rastergis

roi_vec = "../02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
roi_lyr = "gmw_change_site_bboxs_ids"

roi_ids = rsgislib.vectorattrs.read_vec_column(roi_vec, roi_lyr, "roi_id")

versions = ["313", "314", "315"]
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

for version in versions:

    for roi_id in roi_ids:
        print(f"site: {roi_id}")
        out_dir = f"../00_data/08_site_chng_maps/v{version}/site_{roi_id}"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for base_year in gmw_years:
            print(f"\tBase Year: {base_year}")
            base_img = os.path.join(f"../00_data/07_site_maps/{version}/{base_year}", f"gmw_{base_year}_v{version}_site_{roi_id}.kea")
            for chng_year in gmw_years:
                print(f"\t\tChange Year: {chng_year}")
                chng_img = os.path.join(f"../00_data/07_site_maps/{version}/{chng_year}", f"gmw_{chng_year}_v{version}_site_{roi_id}.kea")
                if base_year == chng_year:
                    continue
                elif base_year < chng_year:
                    out_img = os.path.join(out_dir, f"gmw_chng_site_{roi_id}_{base_year}_{chng_year}.kea")
                    band_defns = list()
                    band_defns.append(rsgislib.imagecalc.BandDefn('base', base_img, 1))
                    band_defns.append(rsgislib.imagecalc.BandDefn('chng', chng_img, 1))
                    exp = """(base==1)&&(chng==1)?1:
                             (base==2)&&(chng==2)?2:
                             (base==1)&&(chng==2)?3:
                             (base==2)&&(chng==1)?4:0
                    """
                    rsgislib.imagecalc.band_math(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
                    rsgislib.rastergis.pop_rat_img_stats(out_img, True, True, True)
                    rsgislib.rastergis.set_class_names_colours(out_img, "class_names", class_info_dict)
                else:
                    print("Skipped")
                    #break
