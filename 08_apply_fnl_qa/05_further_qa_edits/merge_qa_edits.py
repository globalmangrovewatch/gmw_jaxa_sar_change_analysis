import rsgislib.vectorutils


not_mng_lyrs = ["peteQA/rm_mangroves.gpkg", "../01_rm_rgns/gmw_v3_qa_rm_rgns.geojson", "lammertQA/v309-never-mangrove.gpkg", "tomQA/Polygons.shp"]
#rsgislib.vectorutils.merge_vectors_to_gpkg(not_mng_lyrs, "../07_apply_fnl_qa_edits/rm_mangroves.gpkg", "rm_mangroves", False)


add_mng_lyrs = ["lammertQA/v309-missing-mangrove.gpkg", "lammertQA/mng-gap-fill-somalia-QA.gpkg", "lammertQA/mng-gap-fill-indonesia-QA.gpkg", "peteQA/add_mangroves.gpkg", "peteQA/add_further_mangroves.gpkg", "akeQA/QA_Ramsar_Sites_Oct2021_part2/Ramsar_Sites_Oct2021_part2.shp", "akeQA/Ramsar_Sites_Oct2021_part-1/Ramsar_Sites_Oct2021_part-1.shp"]
rsgislib.vectorutils.merge_vectors_to_gpkg(add_mng_lyrs, "../07_apply_fnl_qa_edits/add_mangroves.gpkg", "add_mangroves", False)