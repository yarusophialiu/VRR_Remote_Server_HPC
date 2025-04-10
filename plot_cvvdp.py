import os
import numpy as np
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt



def type1(df, label_idx, number, refresh_rate, bitrate, max_x, max_y, SAVE = False):
    """x axis is bandwidth, y axis is JOD, color is resolution"""
    bitrate_df = df.iloc[label_idx, 0] # check if bitrate is correct
    print(f'bitrate_df {bitrate_df}')
    if DEBUG:
        print(f'bitrate_df {bitrate_df}, bitrate {bitrate}')

    assert bitrate_df == bitrate

    fig, ax = plt.subplots(figsize=(8, 5))
    labels = ['360p', '480p', '720p', '864p', '1080p']
    speeds_dict = {1: 'Slow', 2: 'Medium', 3: 'Fast'}
    bitrates_mapping = {1000: '1 Mbps', 1500: '1.5 Mbps', 2000: '2 Mbps', 3000: '3 Mbps', 4000: '4 Mbps'}
    # colors = ['blue', 'greenyellow', 'red', 'green', 'orange',]
    # colors = ['blue', 'greenyellow', 'red', 'gray', 'cyan', 'green', 'orange',]

    # collect data for each resolution
    # manually skip the resolution we dont want
    resolution_not_want = ['540p']
    for i, resolution in enumerate(labels):
        # print(f'\n\n\ni resolution {i, resolution}')
        if resolution in resolution_not_want:
            continue

        jod = []
        for num in range(0, number): # e.g. first 3 fps, i.e. 30, 60, 70

            val = df.iloc[label_idx, 1+i+5*num]
            jod.append(val)
        jod = [float(v) for v in jod]        
        # print(f'resolution {resolution}, jod {jod}, label {labels[i]}')
        # print(f'max_y {max_y} in jod: {max_y in jod}')
        ax.plot(refresh_rate, jod, marker='o', label=labels[i], linestyle='-', color=colors[i])
        # ax.text(max_x + 0.05, max_y + 0.08, f"{resolution}p {max_x}Hz", color=colors[i], fontsize=10, ha='left', va='bottom')


        # Highlight the max point on the current resolution curve
        if max_y in jod:
            print(f'find max')
            ax.scatter(max_x, max_y, color=colors[i], s=200, marker='o', zorder=5)  # Large triangle
            ax.text(max_x - 0.01, max_y + 0.1, f"{resolution} {max_x}Hz", color='grey', fontsize=11, ha='right', va='bottom')

    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Framerate (Hz)', fontsize=15)
    ax.set_xticks(refresh_rate)
    ax.set_ylabel('Quality (JOD)', fontsize=15, rotation=90)
    # ax.set_title(f'{sppeds_dict[speed]} speed - {bitrate/1000} Mbps', fontsize=13)
    ax.set_title(f'ColorVideoVDP results, {scene_name}_{sheet_name} {bitrates_mapping[bitrate]}', fontsize=13)
    ax.grid(True, color='lightgrey', linestyle='--')
    ax.legend(fontsize=10)

    if SAVE:
        p1 = f'{scene_output_dir}/plot1'
        os.makedirs(p1, exist_ok=True)
        img_path = f"{p1}/p1_{scene_name}_{sheet_name}_{bitrate}.svg"
        if not os.path.exists(img_path):
            fig.savefig(img_path, bbox_inches='tight', pad_inches=0.1)
            print(f"File saved: {img_path}")
        else:
            print(f"File already exists: {img_path}")
        # plt.savefig(f"{p1}/p1_{scene_name}_{sheet_name}_{bitrate}.png")
    if SHOW:
        plt.show()


def type2(df, label_idx, bitrate, number, refresh_rate, SAVE = False):
    """
    x axis is resolution, y axis is JOD, color is bitrate, labels are refresh rate
    number is len(refresh_rate)
    """
    bitrate_df = df.iloc[label_idx, 0] # check if bitrate is correct
    if DEBUG:
        print(f'bitrate_df {bitrate_df}, bitrate {bitrate}')

    x_values = np.array([1080, 864, 720, 480, 360,]) # resolution
    x_values = sorted(x_values)
    # print(f'\n\n\n')
    # fig, ax = plt.subplots(figsize=(8, 5))
    for num in range(number): # loop column
        # cvvdp jod from file1
        jod_cvvdp = df.iloc[label_idx, 1+5*num:6+5*num].values # get cvvdp for each refresh rate
        jod_cvvdp = [float(v) for v in jod_cvvdp]   
        # print(f'jod_cvvdp {jod_cvvdp}')     
        # max_jod = max(jod_cvvdp)
        # # Find values within 0.25 range of the maximum
        # close_to_max = [value for value in jod_cvvdp if abs(max_jod - value) <= 0.25]
        # print("Maximum JOD:", max_jod)
        # print("Values within 0.25 range of the maximum:", close_to_max)

        # print(f'idx {num}, fps{refresh_rate[num]}, JOD {jod_cvvdp}, ') # max JOD {max(jod_cvvdp)}
        max_jod_idx = np.argmax(jod_cvvdp)
        # print(f'idx {num}, fps{refresh_rate[num]}, JOD {jod_cvvdp}, max JOD {max(jod_cvvdp)}')
        max_jod.append(max(jod_cvvdp))
        max_res.append(x_values[max_jod_idx])

    #     ax.plot(x_values, jod_cvvdp, marker='o', label=f'{refresh_rate[num]} fps')
    #     ax.set_xticks(x_values)

    # ax.set_xlabel('Resolution')
    # ax.set_ylabel('JOD')
    # ax.set_title(f'CVVDP - scene {scene_name} - path{path}_seg{seg}, speed {speed} - {bitrate} kbps')
    # ax.grid(True)
    # ax.legend()
    # if SAVE:
    #     p2 = f'{scene_output_dir}/plot2'
    #     os.makedirs(p2, exist_ok=True)
    #     img_path = f"{p2}/p2_{scene_name}_{sheet_name}_{bitrate}.png"
    #     if not os.path.exists(img_path):
    #         fig.savefig(img_path)
    #         print(f"File saved: {img_path}")
    #     else:
    #         print(f"File already exists: {img_path}")
    #     # fig.savefig(f"{p2}/p2_{scene_name}_{sheet_name}_{bitrate}.png")
    # if SHOW:
    #     plt.show()



# download cvvdp results from HPC
# process results by running this file
# write to excel using write_excel.py
# plot using plot_cvvdp.py

# suitable for excel written using program, e.g. suntemple-05-03, sheetname fast, with 30-120fps
# Plot cvvdp results from csv file
# in type 2 change 2+6*num:9+6*num to 2+7*num:9+7*num if has 676 column
if __name__ == "__main__":
    SAVE = False # True, False
    SHOW = True
    DEBUG = False

    refresh_rate = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    y_min, y_max = 5, 9.25 # 4.25, 7.5 
    bitrate_dict = {1000: 0, 1500: 1, 2000: 2, 3000: 3, 4000: 4}
    bitrates = [1000, 1500, 2000, 3000, 4000]
    bitrates = [1000]

    # colors = ['deepskyblue', 'lime', 'red', 'forestgreen', 'orange',] # dodgerblue
    colors = ['deepskyblue', 'gold', 'salmon', 'palegreen', 'plum',] # dodgerblue darkorange
    
    SCENES = ['bedroom', 'bistro', 'crytek_sponza', 'gallery', 'living_room', \
        'lost_empire', 'room', 'sibenik', 'suntemple', 'suntemple_statue']

    SCENES = ['bedroom',]
    excel_date = '2025-04-07' # '400_700_900kbps'
    
    for scene_name in SCENES:
        print(f'\n\n\n================================== SCENE {scene_name} ==================================')
        file_path = f'excel/data-{excel_date}/{scene_name}.xlsx'
        for path in range(1, 2):
            for seg in range(1, 2):
                same_seg_different_speed = {}
                for speed in range(1, 2): # 4
                    if SAVE:
                        today = date.today()
                        scene_output_dir = f'cvvdp_plots/plot-{today}/{scene_name}'
                        os.makedirs(scene_output_dir, exist_ok=True)

                    sheet_name = f'path{path}_seg{seg}_{speed}'
                    df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=['NA'])
                    print(f'============================ sheet_name {sheet_name} ============================')
                    for bitrate in bitrates:
                        # print(f'bitrate {bitrate}')
                        print(f'================= bitrate {bitrate} kbps =================')
                        max_jod = []
                        max_res = []
                        type2(df, bitrate_dict[bitrate], bitrate, len(refresh_rate), refresh_rate, SAVE)
                        print(f'max_jod {max_jod}')
                        max_idx = np.argmax(max_jod) # only availble if type2 is run
                        # print(f'\nmax_res {max_res}')
                        print(f'bitrate {bitrate}, max JOD is {max_jod[max_idx]} with resolution {max_res[max_idx]} fps {refresh_rate[max_idx]}\n')
                        type1(df, bitrate_dict[bitrate], len(refresh_rate), refresh_rate, bitrate, refresh_rate[max_idx], max_jod[max_idx], SAVE)
                        # break