singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python calc_pxl_stats.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_1996/*.kea"
-o gmw_v3_mng_mjr_ext_1996.json