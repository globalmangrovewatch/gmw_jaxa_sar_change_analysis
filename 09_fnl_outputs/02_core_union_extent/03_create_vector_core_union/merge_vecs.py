import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_v3_mjr_union_core_v314.gpkg"

# Union
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_summaries/gmw_v3_union_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_union", False)

# Core
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_summaries/gmw_v3_core_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_core", True)



