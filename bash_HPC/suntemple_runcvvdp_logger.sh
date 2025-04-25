#!/bin/bash

#SBATCH -J suncvvdp
#SBATCH -A MANTIUK-SL3-GPU
#SBATCH -p ampere
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH -o logs/tmp_%a.log

#SBATCH --time=01:00:00
#SBATCH -a 1-45 # TODO: change job array id

scene="suntemple" # TODO: change scene

numnodes=$SLURM_JOB_NUM_NODES
numtasks=$SLURM_NTASKS
mpi_tasks_per_node=$(echo "$SLURM_TASKS_PER_NODE" | sed -e  's/^\([0-9][0-9]*\).*$/\1/')


source $HOME/cvvdp_v2/bin/activate
module load ceuadmin/ffmpeg/5.1.1

echo "Number of nodes allocated: $numnodes"
echo "Total number of tasks: $numtasks"
echo "MPI tasks per node: $mpi_tasks_per_node"
echo "The current scene is: $scene"

logfile="logs/${scene}/cvvdp_logger_${SLURM_ARRAY_TASK_ID}.log"
mkdir -p "$(dirname "$logfile")"  # Ensure folder exists
exec > "$logfile" 2>&1


#! Work directory (i.e. where the job will run):
workdir="$SLURM_SUBMIT_DIR"  # The value of SLURM_SUBMIT_DIR sets workdir to the directory
                             # in which sbatch is run.

#! Number of MPI tasks to be started by the application per node and in total (do not change):
np=$[${numnodes}*${mpi_tasks_per_node}]

cd $workdir
echo -e "Changed directory to `pwd`.\n"

JOBID=$SLURM_JOB_ID

echo -e "JobID: $JOBID\n======"
echo "Argument: $options"
echo "Time: `date`"
echo "Running on master node: `hostname`"
echo "Current directory: `pwd`"

echo -e "\nnumtasks=$numtasks, numnodes=$numnodes, mpi_tasks_per_node=$mpi_tasks_per_node"
echo -e "\nExecuting command:\n==================\n$CMD\n"

today=$(date +%F)  # Formats to YYYY-MM-DD
directory_name="/home/yl962/rds/hpc-work/VRR/cvvdp_results/${today}/${scene}"
# directory_name="/home/yl962/rds/hpc-work/VRR/cvvdp_results/${scene}"
mkdir -p "$directory_name"
filename="${directory_name}/${scene}_logger_${SLURM_ARRAY_TASK_ID}.txt"
touch "$filename"
python runcvvdp_logger.py $SLURM_ARRAY_TASK_ID $scene > "$filename" 

echo -e "\nRun metric finished\n"
date