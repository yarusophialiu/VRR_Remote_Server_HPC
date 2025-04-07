from math import *

def mapIdToPath(id):
    """
    NOTE: input id starts from 0 not 1, HPC job id starts from 1
    so should be mapIdToPath(JOBID-1)

    we run 45 jobs/tasks (allocate 13 gpus) at one time as each scene has 45 clips
    so we run 10 times as there are in total 10 scenes
    for each task id, we run videos for 1 scene, 1 seg, 1 speed, i.e. for loop 5 * 10 = 50 videos
    e.g. sbatch --array=1-10:1 -A STARS-SL3-GPU submission_script

    id is from 0-44, map id -> path, seg, speed

    e.g. id 0 -> paths[0], segs[0], speeds[0]
         id 1 -> paths[0], segs[0], speeds[1]
    Note that id in HPC starts from 1, so delete id by 1 when call the function
    mapIdToPath(0) -> (1, 1, 1) path1 seg1 speed1
    mapIdToPath(16) -> (2, 3, 2) path2 seg3 speed2
    """
    pathIdx = int(floor(id/9))
    segIdx = int(floor((id - pathIdx * 9) / 3))
    speedIdx = (id - pathIdx * 9) % 3
    paths = [1, 2, 3, 4, 5]
    segs = [1, 2, 3,]
    speeds = [1, 2, 3,]
#    print(f'pathIdx {pathIdx}, segIdx {segIdx} speedIdx {speedIdx}')
    return paths[pathIdx], segs[segIdx], speeds[speedIdx]

