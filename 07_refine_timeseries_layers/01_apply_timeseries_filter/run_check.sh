#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check


singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2007_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2008_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2009_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2010_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2015_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2016_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2017_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2018_tpflt/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_2019_tpflt/*.kea"


