#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check


singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2007_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2008_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2009_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2010_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2015_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2016_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2017_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2018_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2019_v312/*.tif"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py \
--nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2020_v312/*.tif"
