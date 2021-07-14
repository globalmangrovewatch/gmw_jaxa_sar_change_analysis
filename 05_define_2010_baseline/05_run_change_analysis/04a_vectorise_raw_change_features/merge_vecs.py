import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_raw_2010_chngs_feats_vecs.gpkg"

# 2010
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2010_chngs_vecs/*2010_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2010_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2010_chngs_vecs/*2010_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2010_mng", True)







