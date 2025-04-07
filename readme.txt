Everything happens on HPC cluster

embed h265 into mp4
run cvvdp on test and reference videos

on HPC
h265 are saved in /home/yl962/rds/hpc-work/VRR/VRRMP4/h265 
each scene has 11250 videos
convert h265 to mp4 is in /home/yl962/rds/hpc-work/VRR/convert_h265
cvvdp results are saved in /home/yl962/rds/hpc-work/VRR/logs/cvvdp_results_500_2000kbps/bedroom/bedroom_10.txt

call this before using ffmpeg
module load ceuadmin/ffmpeg/5.1.1


nano: (ctr o enter ctr x)

steps
upload h265 videos to VRRMP4/h265
wsl
kinit yl962@DC.CL.CAM.AC.UK
rsync -avzP crytek_sponza gallery living_room lost_empire yl962@login-icelake.hpc.cam.ac.uk:/home/yl962/rds/hpc-work/VRR/VRRMP4/h265
(rsync resume from lost connection, better than scp)
under convert_h265, change id, sbatch embedh265.py


HPC command
squeue -u yl962
find . -type f | wc -l 
dos2unix runcvvdp.sh

print in python file, echo in bash file, will be saved into xxx.log


(base) [yl962@login-q-2 run_cvvdp]$ squeue -u yl962
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
    7901225_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (None)
    7901222_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (None)
    7901220_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (Priority)
    7901219_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (Priority)
    7901217_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (Priority)
    7901216_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (Priority)
    7901215_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (Priority) crytek_sponza
    7901079_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (Priority) bistro
    7901074_[1-45]    ampere    cvvdp    yl962 PD       0:00      1 (Priority) bedroom
