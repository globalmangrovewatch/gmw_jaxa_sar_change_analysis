singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-beta-dev.sif createdb pbpt_gmw_db 
singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-beta-dev.sif psql -d pbpt_gmw_db --host 10.212.33.77

#CREATE USER admin WITH PASSWORD '4RPeBt84';
#GRANT ALL PRIVILEGES ON DATABASE pbpt_gmw_db TO admin;

