import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2015_v3_vecs.gpkg"

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2015_v3_vecs/*_v3_init.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_init_2015_v3", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2015_v3_vecs/*2015_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_2015_2010_loss", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2015_v3_vecs/*2015_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_2015_2010_gain", True)



