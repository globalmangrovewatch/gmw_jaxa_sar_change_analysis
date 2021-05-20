import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2008_v3.gpkg"

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2008_v3_fnl_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_2008_v3", False)



