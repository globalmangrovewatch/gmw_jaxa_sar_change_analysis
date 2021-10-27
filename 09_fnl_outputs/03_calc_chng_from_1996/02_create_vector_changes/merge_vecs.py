import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_v3_mjr_chng_f1996_v312.gpkg"

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2007_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2007", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2008_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2008", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2009_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2009", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2010_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2010", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2015_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2015", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2016_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2016", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2017_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2017", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2018_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2018", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2019_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2019", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2020_v312_vecs/*.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "f1996_t2020", False)
