#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check


singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_1996_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2007_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2008_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2009_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2010_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2015_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2016_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2017_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2018_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2019_v311/*.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_min_2020_v311/*.kea"
