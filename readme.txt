Everything happens on HPC cluster, then process cvvdp_results obtained from HPC

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


Process cvvdp_results from HPC
clean_cvvdp_results.py
write_excel.py



(base) [yl962@login-q-2 run_cvvdp]$ squeue -u yl962
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
    7942865_[1-45]    ampere lost_emp    yl962 PD       0:00      1 (None) lost_empire
(base) [yl962@login-q-3 run_cvvdp]$ squeue -u yl962
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
        7991099_10    ampere    le_10    yl962 PD       0:00      1 (ReqNodeNotAvail, UnavailableNodes:gpu-q-[2-47])
   8005539_[11-20]    ampere    11_20    yl962 PD       0:00      1 (None)


cvvdp --test .mp4 --ref .mp4 --display standard_fhd --full-screen-resize bilinear --temp-resample
