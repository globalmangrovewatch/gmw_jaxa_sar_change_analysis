import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_v3_mjr_chng_f1996_v314.gpkg"

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2007_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2007", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2008_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2008", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2009_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2009", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2010_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2010", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2015_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2015", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2016_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2016", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2017_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2017", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2018_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2018", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2019_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2019", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2020_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "f1996_t2020", True)
