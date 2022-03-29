import os
import tqdm

import numpy
import rsgislib.tools.utils
import rsgislib.vectorattrs
import rsgislib.rastergis

roi_vec = "../../10_acc_assess/02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
roi_lyr = "gmw_change_site_bboxs_ids"

roi_ids = rsgislib.vectorattrs.read_vec_column(roi_vec, roi_lyr, "roi_id")

gmw_years = [1996, 2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]
n_years = len(gmw_years)

class_names_dict = dict()
class_names_dict[1] = "Mangroves"
class_names_dict[2] = "Not Mangroves"
class_names_dict[3] = "Mangroves > Not Mangroves"
class_names_dict[4] = "Not Mangroves > Mangroves"

chng_m_nm_areas = dict()
chng_nm_m_areas = dict()

chng_m_nm_areas["sites"] = roi_ids
chng_nm_m_areas["sites"] = roi_ids
chng_m_nm_areas["clmp_size"] = dict()
chng_nm_m_areas["clmp_size"] = dict()

for clmp_size in tqdm.tqdm([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
    chng_m_nm_areas["clmp_size"][clmp_size] = dict()
    chng_nm_m_areas["clmp_size"][clmp_size] = dict()

    for i, base_year in enumerate(gmw_years):
        #print(f"\tBase Year: {base_year}")
        if i < n_years - 1:
            chng_year = gmw_years[i + 1]
            #print(f"\t\tChange Year: {chng_year}")

            chng_m_nm_areas["clmp_size"][clmp_size][chng_year] = list()
            chng_nm_m_areas["clmp_size"][clmp_size][chng_year] = list()

            for roi_id in roi_ids:
                #print(f"site: {roi_id}")
                chngs_dir = f"../00_data/03_site_chng_maps_clumps/site_{roi_id}"

                chng_clumps_img = os.path.join(chngs_dir, f"gmw_chng_site_{roi_id}_{base_year}_{chng_year}.kea")

                hist_col = rsgislib.rastergis.get_column_data(chng_clumps_img, "Histogram")
                chng_cls_col = rsgislib.rastergis.get_column_data(chng_clumps_img, "chng_cls")
                area_ha_col = rsgislib.rastergis.get_column_data(chng_clumps_img, "area_ha")

                area_ha_m_nm = area_ha_col[(chng_cls_col == 3) & (hist_col > clmp_size)]
                chng_m_nm_areas["clmp_size"][clmp_size][chng_year].append(float(numpy.sum(area_ha_m_nm)))
                area_ha_nm_m = area_ha_col[(chng_cls_col == 4) & (hist_col > clmp_size)]
                chng_nm_m_areas["clmp_size"][clmp_size][chng_year].append(float(numpy.sum(area_ha_nm_m)))

rsgislib.tools.utils.write_dict_to_json(chng_m_nm_areas, "chng_areas_mangroves_notmangroves.json")
rsgislib.tools.utils.write_dict_to_json(chng_nm_m_areas, "chng_areas_notmangroves_mangroves.json")
