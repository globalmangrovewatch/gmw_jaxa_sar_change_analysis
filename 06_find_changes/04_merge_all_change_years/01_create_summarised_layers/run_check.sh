#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_1996/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2007/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2008/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2009/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2010/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2015/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2016/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2017/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2018/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2019/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_2020/*.tif"



