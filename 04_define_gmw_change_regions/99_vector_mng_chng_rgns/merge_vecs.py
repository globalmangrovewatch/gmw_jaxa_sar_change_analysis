import glob
import rsgislib.vectorutils

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/other_base_data/gmw_v2_chng_from_2010_vecs/*.gpkg")

out_file = "/scratch/a.pfb/gmw_v3_change/data/other_base_data/gmw_v2_chng_from_2010_vecs.gpkg"

rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_v2_chng_from_2010_vecs", False)


input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/other_base_data/gmw_v2_chng_from_2010_buf_vecs/*.gpkg")

out_file = "/scratch/a.pfb/gmw_v3_change/data/other_base_data/gmw_v2_chng_from_2010_buf_vecs.gpkg"

rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_v2_chng_from_2010_buf_vecs", False)





