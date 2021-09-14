import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_304_2010base_vecs.gpkg"

# 1996
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_1996_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_1996", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_1996_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_1996", True)

# 2007
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2007_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2007", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2007_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2007", True)

# 2008
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2008_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2008", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2008_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2008", True)

# 2009
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2009_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2009", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2009_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2009", True)

# 2015
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2015_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2015", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2015_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2015", True)

# 2016
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2016_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2016", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2016_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2016", True)

# 2017
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2017_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2017", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2017_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2017", True)

# 2018
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2018_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2018", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2018_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2018", True)

# 2019
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2019_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2019", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2019_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2019", True)

# 2020
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_2020_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2020", True)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_2020_v3_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "pchg_2020", True)






