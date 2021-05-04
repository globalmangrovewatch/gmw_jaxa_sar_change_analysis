import glob
import rsgislib.vectorutils

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_change_regions_vecs/*.gpkg")

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_change_regions.gpkg"

rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_v3_init_chng_rgns", False)