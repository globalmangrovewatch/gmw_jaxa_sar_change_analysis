import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_v312.gpkg"

# 1996
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_1996_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_1996", False)

# 2007
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2007_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2007", True)

# 2008
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2008_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2008", True)

# 2009
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2009_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2009", True)

# 2010
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2010_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2010", True)

# 2015
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2015_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2015", True)

# 2016
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2016_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2016", True)

# 2017
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2017_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2017", True)

# 2018
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2018_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2018", True)

# 2019
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2019_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2019", True)

# 2020
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2020_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_mjr_2020", True)







