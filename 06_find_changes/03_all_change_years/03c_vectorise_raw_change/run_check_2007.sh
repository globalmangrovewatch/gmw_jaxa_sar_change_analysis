#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_1996_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2008_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2009_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2010_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2015_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2016_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2017_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2018_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2019_chngs_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2007/gmw_2007_2020_chngs_vecs/*.gpkg"
