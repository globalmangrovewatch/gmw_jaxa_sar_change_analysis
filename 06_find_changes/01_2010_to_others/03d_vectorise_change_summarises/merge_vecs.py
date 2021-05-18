import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_chng_sum_pre2010_vecs.gpkg"

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_pre_2010_chngs_vecs/*_sum_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pre_2010_mng_loss", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_pre_2010_chngs_vecs/*_sum_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pre_2010_mng_gain", True)


out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_chng_sum_post2010_vecs.gpkg"

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_post_2010_chngs_vecs/*_sum_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "post_2010_mng_gain", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_post_2010_chngs_vecs/*_sum_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "post_2010_mng_loss", True)
