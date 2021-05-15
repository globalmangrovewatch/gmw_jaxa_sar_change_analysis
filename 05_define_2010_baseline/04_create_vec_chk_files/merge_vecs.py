import glob
import rsgislib.vectorutils

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3_vecs/*.gpkg")
out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3_vecs.gpkg"
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_2010_v3", False)


input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn_vecs/*.gpkg")
out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn_vecs.gpkg"
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_2010_potent_chng", False)


input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_stats_rgn_vecs/*.gpkg")
out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_stats_rgn_vecs.gpkg"
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "gmw_2010_potent_chng_stats_rgns", False)


