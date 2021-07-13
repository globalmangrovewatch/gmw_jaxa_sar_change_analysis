singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_hdf5_files.py --rmerr --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2010_pxl_vals/*.h5"




