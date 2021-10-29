singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/rm_files_gt_size.py \
-s 1000000 --rmfile -i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_summaries/gmw_v3_union_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/rm_files_gt_size.py \
-s 1000000 --rmfile -i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_summaries/gmw_v3_core_v312/*.tif"
