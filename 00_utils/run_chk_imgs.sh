singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2020/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2019/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2018/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2017/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2016/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2015/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2009/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2008/*/*db_mskd_reg.kea"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
--nbands 3 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2007/*/*db_mskd_reg.kea"

#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
#/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
#--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
#-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2020_chngs/*mng_chng.kea"


#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
#/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
#--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
#-i "/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn/*.kea"

#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
#/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python chk_imgs.py \
#--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 1  --printerrs \
#-i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2010_chngs/*mng_chng.kea"