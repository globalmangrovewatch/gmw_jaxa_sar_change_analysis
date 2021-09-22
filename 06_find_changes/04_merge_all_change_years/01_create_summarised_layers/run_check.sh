#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2007_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2008_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2009_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2010_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2015_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2016_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2017_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2018_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2019_mng_ext/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from1996/gmw_base1996_2020_mng_ext/*.kea"

