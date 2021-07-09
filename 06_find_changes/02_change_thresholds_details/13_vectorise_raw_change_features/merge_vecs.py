import glob
import rsgislib.vectorutils

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_raw_chngs_feats_vecs.gpkg"

# 1996
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_1996_chngs_vecs/*1996_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_1996_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_1996_chngs_vecs/*1996_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_1996_mng", True)

# 2007
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2007_chngs_vecs/*2007_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2007_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2007_chngs_vecs/*2007_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2007_mng", True)

# 2008
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2008_chngs_vecs/*2008_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2008_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2008_chngs_vecs/*2008_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2008_mng", True)

# 2009
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2009_chngs_vecs/*2009_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2009_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2009_chngs_vecs/*2009_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2009_mng", True)

# 2015
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2015_chngs_vecs/*2015_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2015_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2015_chngs_vecs/*2015_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2015_mng", True)

# 2016
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2016_chngs_vecs/*2016_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2016_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2016_chngs_vecs/*2016_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2016_mng", True)

# 2017
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2017_chngs_vecs/*2017_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2017_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2017_chngs_vecs/*2017_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2017_mng", True)

# 2018
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2018_chngs_vecs/*2018_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2018_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2018_chngs_vecs/*2018_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2018_mng", True)

# 2019
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2019_chngs_vecs/*2019_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2019_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2019_chngs_vecs/*2019_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2019_mng", True)

# 2020
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2020_chngs_vecs/*2020_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2020_nmng", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2020_chngs_vecs/*2020_not_mng_chng.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2020_mng", True)


print("Starting Upper Merge")

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_raw_chngs_upper_feats_vecs.gpkg"

# 1996
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_1996_chngs_vecs/*1996_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_1996_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_1996_chngs_vecs/*1996_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_1996_mng_upper", True)

# 2007
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2007_chngs_vecs/*2007_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2007_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2007_chngs_vecs/*2007_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2007_mng_upper", True)

# 2008
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2008_chngs_vecs/*2008_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2008_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2008_chngs_vecs/*2008_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2008_mng_upper", True)

# 2009
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2009_chngs_vecs/*2009_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2009_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2009_chngs_vecs/*2009_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2009_mng_upper", True)

# 2015
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2015_chngs_vecs/*2015_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2015_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2015_chngs_vecs/*2015_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2015_mng_upper", True)

# 2016
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2016_chngs_vecs/*2016_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2016_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2016_chngs_vecs/*2016_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2016_mng_upper", True)

# 2017
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2017_chngs_vecs/*2017_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2017_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2017_chngs_vecs/*2017_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2017_mng_upper", True)

# 2018
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2018_chngs_vecs/*2018_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2018_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2018_chngs_vecs/*2018_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2018_mng_upper", True)

# 2019
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2019_chngs_vecs/*2019_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2019_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2019_chngs_vecs/*2019_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2019_mng_upper", True)

# 2020
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2020_chngs_vecs/*2020_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2020_nmng_upper", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2020_chngs_vecs/*2020_not_mng_chng_upper.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2020_mng_upper", True)



print("Starting Lower Merge")

out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_raw_chngs_lower_feats_vecs.gpkg"

# 1996
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_1996_chngs_vecs/*1996_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_1996_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_1996_chngs_vecs/*1996_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_1996_mng_lower", True)

# 2007
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2007_chngs_vecs/*2007_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2007_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2007_chngs_vecs/*2007_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2007_mng_lower", True)

# 2008
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2008_chngs_vecs/*2008_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2008_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2008_chngs_vecs/*2008_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2008_mng_lower", True)

# 2009
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2009_chngs_vecs/*2009_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2009_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2009_chngs_vecs/*2009_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2009_mng_lower", True)

# 2015
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2015_chngs_vecs/*2015_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2015_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2015_chngs_vecs/*2015_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2015_mng_lower", True)

# 2016
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2016_chngs_vecs/*2016_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2016_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2016_chngs_vecs/*2016_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2016_mng_lower", True)

# 2017
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2017_chngs_vecs/*2017_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2017_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2017_chngs_vecs/*2017_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2017_mng_lower", True)

# 2018
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2018_chngs_vecs/*2018_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2018_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2018_chngs_vecs/*2018_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2018_mng_lower", True)

# 2019
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2019_chngs_vecs/*2019_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2019_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2019_chngs_vecs/*2019_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2019_mng_lower", True)

# 2020
input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2020_chngs_vecs/*2020_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_mng_2020_nmng_lower", False)

input_vecs = glob.glob("/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2020_chngs_vecs/*2020_not_mng_chng_lower.gpkg")
rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "2010_nmng_2020_mng_lower", True)








