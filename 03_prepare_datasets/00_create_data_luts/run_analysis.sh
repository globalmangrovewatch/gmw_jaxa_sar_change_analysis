singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif rsgisbuildimglut.py -i "/scratch/a.pfb/SRTM/extracted/*.hgt" \
-o /scratch/a.pfb/gmw_v3_change/data/other_base_data/global_srtm_lut.gpkg --veclyr srtm --vecformat GPKG

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif rsgisbuildimglut.py -i "/scratch/a.pfb/gmw_v3_change/data/other_base_data/bathymetry/*.tif" \
-o /scratch/a.pfb/gmw_v3_change/data/other_base_data/global_bathymetry_lut.gpkg --veclyr bathymetry --vecformat GPKG

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif rsgisbuildimglut.py -i "/scratch/a.pfb/gmw_v3_change/data/other_base_data/water_occurance/*.tif" \
-o /scratch/a.pfb/gmw_v3_change/data/other_base_data/global_water_occurance_lut.gpkg --veclyr water_occurance --vecformat GPKG
