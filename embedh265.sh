#!/bin/bash
#SBATCH -J embedh265
#SBATCH -A MANTIUK-SL3-CPU

#SBATCH -D /home/yl962/rds/hpc-work/VRR/convert_h265
#SBATCH -o logs/embedh265_%a.log
#SBATCH -c 1
#SBATCH --mem=1G
#SBATCH -t 00:40:00 # Time limit (hh:mm:ss)
#SBATCH -a 9-10

module load ceuadmin/ffmpeg/5.1.1

# output=$(ffmpeg -codecs | grep "hevc")
echo "This task number $SLURM_ARRAY_TASK_ID"
echo "Using $SLURM_CPUS_PER_TASK CPUs cores"
echo

python embedh265.py $SLURM_ARRAY_TASK_ID
