singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2_vec/*.gpkg"





