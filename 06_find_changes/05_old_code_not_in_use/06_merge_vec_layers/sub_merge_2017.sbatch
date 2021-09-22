#!/bin/bash --login

#SBATCH --account=scw1376
#SBATCH --partition=compute
#SBATCH --job-name=gmw_merge_2017
#SBATCH --output=/scratch/a.pfb/gmw_v3_change/logs/gmw_merge_2017_log.out.%J
#SBATCH --error=/scratch/a.pfb/gmw_v3_change/logs/gmw_merge_2017_log.err.%J
#SBATCH --time=2-23:59
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16448

module load parallel singularity

export http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"
export https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python merge_2017.py


