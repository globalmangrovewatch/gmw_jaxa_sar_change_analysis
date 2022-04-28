import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_v314.gpkg"

# 1996
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_1996_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_1996", False)

# 2007
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2007_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2007", True)

# 2008
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2008_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2008", True)

# 2009
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2009_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2009", True)

# 2010
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2010_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2010", True)

# 2015
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2015_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2015", True)

# 2016
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2016_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2016", True)

# 2017
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2017_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2017", True)

# 2018
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2018_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2018", True)

# 2019
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2019_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2019", True)

# 2020
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_max_2020_v314_vecs/*.gpkg")
rsgislib.vectorutils.merge_vectors_to_gpkg(input_vecs, out_file, "mng_max_2020", True)







