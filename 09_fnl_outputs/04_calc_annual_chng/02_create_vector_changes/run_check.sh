#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t2007_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2007_t2008_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2008_t2009_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2009_t2010_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2010_t2015_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2015_t2016_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2016_t2017_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2017_t2018_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2018_t2019_v312_vecs/*.gpkg"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind \
/home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_vec_files.py \
--multi --rmerr --chkproj --epsg 4326 --printerrs \
-i "/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f2019_t2020_v312_vecs/*.gpkg"
