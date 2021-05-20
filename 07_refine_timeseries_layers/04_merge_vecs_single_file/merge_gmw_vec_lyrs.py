import rsgislib.vectorutils


in_files =["/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_1996_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2007_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2008_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2009_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2010_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2015_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2016_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2017_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2018_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2019_v3.gpkg",
           "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_2020_v3.gpkg"]


out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_v3_extents.gpkg"
rsgislib.vectorutils.mergeVectors2GPKGIndLyrs(in_files, out_file, rename_dup_lyrs=False, geom_type=None)

