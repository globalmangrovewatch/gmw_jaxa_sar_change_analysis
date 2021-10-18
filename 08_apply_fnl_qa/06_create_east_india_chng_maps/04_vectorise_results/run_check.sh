#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/*_vecs/*.gpkg"
