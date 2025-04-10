import os
import re
from collections import defaultdict


def clean_logger_file(jobid_list, scene, input_scene_path, output_path):
    not_exist = []
    for jobid in jobid_list:
        print(f'===== jobid {jobid} =====')
        input_file_path = f'{input_scene_path}/{scene}_logger_{jobid}.txt'
        output_file_path = f'{cleaned_scene_path}/{scene}_{jobid}.txt'
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        if not os.path.exists(input_file_path):
            not_exist.append(jobid)
            print(f'File {scene}_logger_{jobid}.txt not exist.')

        with open(input_file_path, 'r') as f:
            lines = f.readlines()

        # cleaned_lines = []
        # bitrate = None
        # current_fps = None
        # seen_fps = set()
        header_lines = []
        results = defaultdict(lambda: defaultdict(list))  # bitrate -> fps -> list of cvvdp

        current_bitrate = None
        current_fps = None

        for line in lines:
            if line.startswith("SLURM_ARRAY_TASK_ID") or line.startswith("Scene path"):
                header_lines.append(line.strip())
            elif "bitrate" in line:
                match = re.search(r"bitrate (\d+)", line)
                if match:
                    current_bitrate = match.group(1)
            
            elif "test" in line:
                # Extract fps from filename: bitrate_fps_resolution.mp4
                match = re.search(r"/(\d+)_(\d+)_(\d+)\.mp4", line)
                if match:
                    current_fps = match.group(2)

            elif "cvvdp=" in line:
                match = re.search(r"cvvdp=([\d\.]+)", line)
                # match = re.search(r"cvvdp=([-]?\d+\.\d+)", line)

                if match and current_bitrate and current_fps:
                    results[current_bitrate][current_fps].append(f"cvvdp={match.group(1)} [JOD]")
                    
        # Write cleaned result
        with open(output_file_path, 'w') as f:
            f.write('\n'.join(header_lines) + '\n')
            for bitrate in sorted(results.keys(), key=int):
                f.write(f"========================= bitrate {bitrate} =========================\n")
                for fps in results[bitrate].keys():
                    f.write(f"========================= fps{fps} =========================\n")
                    for val in results[bitrate][fps]:
                        f.write(val + '\n')

    return not_exist


# download cvvdp results from HPC
# process results by running this file
# write to excel using write_excel.py
# plot using plot_cvvdp.py 
if __name__ == "__main__":
    scene_arr = ['bedroom', 'bistro', 'crytek_sponza', 'gallery', 'living_room', \
            'lost_empire', 'room', 'sibenik', 'suntemple', 'suntemple_statue'] # 'lost_empire'
    scene_arr = ['lost_empire']
    # scene_arr = ['bedroom']
    CLEANED_DIR = "cleaned"
    jobid_list = [i for i in range(1, 46)] # 1, 46

    # Run over all logger files in a folder
    for scene in scene_arr:
        input_scene_path = f"cvvdp_results/{scene}"
        cleaned_scene_path = f'{CLEANED_DIR}/{scene}'
        not_exist = clean_logger_file(jobid_list, scene, input_scene_path, cleaned_scene_path)

        if len(not_exist) > 0:
            print(f"Job ids not exist: {not_exist}")
