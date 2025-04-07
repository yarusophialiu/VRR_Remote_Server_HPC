import os
import logging
import subprocess



# make sure on temp-resample branch
def run_cvvdp(reference_path, test_path):
        logging.info(f'\nreference_path {reference_path}')
        logging.info(f'test_path {test_path}\n')

        command = f"cvvdp --test {test_path} --ref {reference_path} --display standard_fhd --full-screen-resize bilinear --temp-resample"

        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            print(result.stdout)
            print("Command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running the command: {e}")

        return result  # TODO:  What is the result, and write to file



def compare_videos(ref_root, test_root):
    for scene in os.listdir(test_root):
        logger.info(f'Scene: {scene}')
        scene_test_path = os.path.join(test_root, scene)

        for seg_folder in os.listdir(scene_test_path):
            seg_test_path = os.path.join(scene_test_path, seg_folder)
            bitrate_folders = os.listdir(seg_test_path)

            # Build reference path
            ref_filename = f"refOutput_{seg_folder}_166_1080.mp4"
            ref_path = os.path.join(ref_root, scene, seg_folder, ref_filename)

            if not os.path.exists(ref_path):
                print(f"Reference not found: {ref_path}")
                continue

            for bitrate in bitrate_folders:
                test_folder = os.path.join(seg_test_path, bitrate)

                for file in os.listdir(test_folder):
                    if file.endswith(".mp4") or file.endswith(".h265"):
                        test_path = os.path.join(test_folder, file)
                        print(f'test_path {test_path}')
                        print(f'ref_path {ref_path}')

                        # TODO: write the result in to txt, organize order
                        result = run_cvvdp(ref_path, test_path)

                        result_filename = os.path.splitext(file)[0] + ".txt"
                        result_path = os.path.join(test_folder, result_filename)

                        with open(result_path, "w") as f:
                            f.write(result)
                    break
                break
            break
        break
                        
if __name__ == "__main__":
    ref_root = r"C:\Users\15142\Projects\VRR\Data\VRRMP4_Reference"
    test_root = r"C:\Users\15142\new\Falcor\Source\Samples\EncodeDecode\encodedH264\2025-03-28"

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger()
    # logger.info(f"SLURM_ARRAY_TASK_ID (renamed to id): {id}")
    compare_videos(ref_root, test_root)