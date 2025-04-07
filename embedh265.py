import os
import subprocess
import argparse
import logging
# from utils import *



def run_encode_command(input_path, frame_rate, output_path):
    cmd = [
        'ffmpeg', '-i', input_path,
        '-r', str(frame_rate),
        '-vcodec', 'copy',
        '-acodec', 'copy',
        output_path
    ]

    # print(f"Converting {input_path} -> {output_path}")
    # subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # subprocess.run(cmd, check=True)
    print(f"Converting to {output_path}")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False



def embed_h265(scene, input_root, output_root):
    failed_encodes = []
    scene_path = os.path.join(input_root, scene)

    for seg in os.listdir(scene_path):
        seg_path = os.path.join(scene_path, seg)

        for bitrate in os.listdir(seg_path):
            bitrate_path = os.path.join(seg_path, bitrate)

            for file in os.listdir(bitrate_path):
                if not file.endswith(".h265"):
                    failed_encodes.append(file)
                    continue

                input_path = os.path.join(bitrate_path, file)
                basename = os.path.splitext(file)[0]  # Removes .h265
                fpsval = int(basename.split('_')[1])

                # Build output path under "mp4/"
                rel_path = os.path.relpath(bitrate_path, input_root)
                output_folder = os.path.join(output_root, rel_path)
                os.makedirs(output_folder, exist_ok=True)

                output_filename = os.path.splitext(file)[0] + ".mp4"
                output_path = os.path.join(output_folder, output_filename)
                # print(f'output_filename {output_filename}')
                # print(f'output_path {output_path}')
                if os.path.exists(output_path):
                    print(f"Skipped (already exists): {output_path}")
                    continue
                # TODO: add framerate
                success = run_encode_command(input_path, fpsval, output_path)
                if not success:
                    print(f"Encoding failed: {input_path}")
                    failed_encodes.append(input_path)
        #         break
        #     break
        # break

    # TODO write failed_encodes to log file
    return failed_encodes



if __name__ == "__main__":
    # HPC
    input_root = r"/home/yl962/rds/hpc-work/VRR/VRRMP4/h265"
    VRR_DATA = r'/home/yl962/rds/hpc-work/VRR/VRRMP4'

    # # local PC
    # input_root = r"C:\Users\15142\new\Falcor\Source\Samples\EncodeDecode\encodedH264\2025-04-04" 
    # VRR_DATA = r'C:\Users\15142\Projects\VRR\Data'

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.info(f"SLURM_ARRAY_TASK_ID (renamed to id): {id}\n\n")


    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('SLURM_ARRAY_TASK_ID', type=str, help='The id of task')
    args = parser.parse_args()
    id = args.SLURM_ARRAY_TASK_ID
    id = int(id)

    scene_arr = ['bedroom', 'bistro', 
             'crytek_sponza', 'gallery', 
             'living_room', 'lost_empire', 
             'room', 'sibenik', 'suntemple', 
             'suntemplestatue']

    output_root = f"{VRR_DATA}/h265_to_mp4"
    scene = scene_arr[id-1] # id starts from 1
    
    logger.info(f"scene: {scene}\n\n")
    
    failed_encodes = embed_h265(scene, input_root, output_root)
    logger.info(f"failed_encodes: {failed_encodes}\n\n")
