import os
import sys
import logging
import subprocess
import argparse
from datetime import datetime
from math import *


def mapIdToPath(id):
    """
    we run 15 jobs/tasks (allocate 13 gpus) at one time, each scene has 45 clips, so we run 3 times
    for each task id, we run videos for 1 scene, 1 seg, 1 speed, i.e. for loop 50 * 13 = 650 videos
    e.g. sbatch --array=0-14:1 -A STARS-SL3-GPU submission_script

    id is from 0-44, map id -> path, seg, speed

    e.g. id 0 -> paths[0], segs[0], speeds[0]
         id 1 -> paths[0], segs[0], speeds[1]
    """
    pathIdx = int(floor(id/9))
    segIdx = int(floor((id - pathIdx * 9) / 3))
    speedIdx = (id - pathIdx * 9) % 3
    paths = [1, 2, 3, 4, 5]
    segs = [1, 2, 3,]
    speeds = [1, 2, 3,]
    return paths[pathIdx], segs[segIdx], speeds[speedIdx]


# make sure on temp-resample branch
def run_cvvdp(reference_path, test_path):
        logging.info(f'\nreference {reference_path}')
        logging.info(f'test {test_path}\n')

        command = f"cvvdp --test {test_path} --ref {reference_path} --display standard_fhd --full-screen-resize bilinear --temp-resample --hold-blur"
        # command = f"cvvdp --test {test_path} --ref {reference_path} --display standard_fhd --full-screen-resize bilinear --temp-resample"

        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            print(result.stdout)
            # logging.info(f'result {result}\n')
            # logging.info(f'result.stdout {result.stdout}\n')
            # logging.info(f'Command executed successfully.\n')
            # print("Command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running the command: {e}")
            # logging.info(f'Error running the command\n')

        # return result  # TODO:  What is the result, and write to file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('SLURM_ARRAY_TASK_ID', type=str, help='The id of task')
    parser.add_argument('scene', type=str, help='scene')
    args = parser.parse_args()
    id = args.SLURM_ARRAY_TASK_ID
    id = int(id)
    scene = args.scene 

    # id = 1
    # scene = 'crytek_sponza'

    id -= 1

    # logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

    logger = logging.getLogger()
    logger.info(f"SLURM_ARRAY_TASK_ID: {id}")

    # HPC
    VRRMP4_Reference = r'/home/yl962/rds/hpc-work/VRR/VRRMP4/reference_videos'
    h265_mp4 = r'/home/yl962/rds/hpc-work/VRR/VRRMP4/h265_to_mp4'

    # # local
    # VRRMP4_Reference = r"C:\Users\15142\Projects\VRR\Data\VRRMP4_Reference"
    # h265_mp4 = r"C:\Users\15142\new\Falcor\Source\Samples\EncodeDecode\encodedH264\2025-04-04"


    path, seg, speed = mapIdToPath(id)
    ref_base_dir = f'{VRRMP4_Reference}/{scene}/{scene}_path{path}_seg{seg}_{speed}'
    test_base_dir = f'{h265_mp4}/{scene}/{scene}_path{path}_seg{seg}_{speed}'
    ref_file = f'{ref_base_dir}/refOutput_{scene}_path{path}_seg{seg}_{speed}_166_1080.mp4'

    logger.info(f'Scene path: {scene}_path{path}_seg{seg}_{speed}')

    bitrates = [1000, 1500, 2000, 3000, 4000]
    # bitrates = [1000, 1500, 2000]


    ref_root = f'{VRRMP4_Reference}/{scene}'
    test_root = f'{h265_mp4}/{scene}'
    
    print(f'Reference file \n {ref_file}')
    for bitrate in bitrates:
            print(f'\n\n========================= bitrate {bitrate} =========================')
            logger.info(f'Processing video with bitrate: {bitrate}kbps')
            folder = os.path.join(f'{test_base_dir}', f'{bitrate}')
            # logging.info(f'folder {folder}')
            items = os.listdir(folder) # ['fps120', 'fps150',]
            items = sorted(items)

            for file in items:
                test_file = os.path.join(folder, file)
                # test_file = r'C:\Users\15142\new\Falcor\Source\Samples\EncodeDecode\encodedH264\2025-04-04\crytek_sponza\crytek_sponza_path1_seg1_1\1000\1000_100_1080.mp4'
                # print(f'file {file}')
                # print(f'ref_file \n {ref_file}')

                run_cvvdp(ref_file, test_file)
    # # python .\runcvvdp.py > test.txt
    # # to output to a file, run command: python .\compare_dec_ref.py >> .\compare_dec_ref.txt