import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_init_1996_v3_vecs.gpkg"

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_1996_v3_vecs/*_v3_init.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_1996_v3_init", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_1996_v3_vecs/*1996_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2010_1996_loss", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_1996_v3_vecs/*1996_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2010_1996_gain", True)
