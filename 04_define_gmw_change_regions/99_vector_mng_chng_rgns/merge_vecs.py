import glob
import rsgislib.vectorutils

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/pot_gmw_chng_ocean_chg_rgns_nasa_gmwv2_updates_vecs/*.gpkg")

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/pot_gmw_chng_ocean_chg_rgns_nasa_gmwv2_updates_vecs.gpkg"

rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pot_gmw_chng_ocean_chg_rgns_nasa_gmwv2_updates_vecs", False)



