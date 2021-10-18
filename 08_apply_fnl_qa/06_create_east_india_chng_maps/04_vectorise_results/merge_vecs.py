import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/gmw_v3_east_india_extent_309.gpkg"

# 1996
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/1996_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_1996", False)

# 2007
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2007_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2007", True)

# 2008
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2008_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2008", True)

# 2009
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2009_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2009", True)

# 2010
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2010_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2010", True)

# 2015
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2015_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2015", True)

# 2016
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2016_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2016", True)

# 2017
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2017_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2017", True)

# 2018
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2018_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2018", True)

# 2019
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2019_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2019", True)

# 2020
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/2020_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_2020", True)







