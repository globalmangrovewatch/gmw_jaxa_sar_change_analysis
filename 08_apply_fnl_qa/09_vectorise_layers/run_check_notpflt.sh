#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_1996_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2007_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2008_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2009_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2010_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2015_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2016_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2017_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2018_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2019_v311_notpflt_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2020_v311_notpflt_vecs/*.gpkg"
