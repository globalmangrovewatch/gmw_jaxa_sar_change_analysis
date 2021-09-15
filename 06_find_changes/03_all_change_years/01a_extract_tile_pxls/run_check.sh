#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2007_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2008_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2009_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2010_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2015_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2016_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2017_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2018_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2019_pxl_vals/*.h5" --rmerr --printerrs

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python  ../../../00_utils/chk_hdf5_files.py \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_1996_2020_pxl_vals/*.h5" --rmerr --printerrs

