import matplotlib.pyplot as plt
import numpy as np
from utils import *
from datetime import datetime
import os



def plot():
    # Map paths (scenes) to unique colors
    dfs_by_bitrate = create_df_within_range(SCENES)
    # print(f'dfs_by_bitrate {dfs_by_bitrate}')
    # Loop over bitrates and plot scatter plots
    for bitrate, data in dfs_by_bitrate.items():
        print(f'bitrate {bitrate}')
        resolutions = data['resolution']
        framerates = data['fps']
        paths = data['path']
        velocities = data['velocity']
        converted_resolutions = resolutions.replace(res_mapping)
        jitter_resolultion = np.random.uniform(-0.08, 0.08, size=len(data))  # Adjust jitter range as needed
        jitter_framerate = np.random.uniform(-3, 3, size=len(data))  # Adjust jitter range as needed
        # resolution_with_jitter = converted_resolutions + jitter_resolultion
        # print(f'resolution_with_jitter {resolution_with_jitter}')
        # print(f'velocities {velocities}')
        # # dot_sizes = np.array(velocities) * 60  # dot_sizes are speed 1, 2, 3 * 60
        colors = [speed_colors[v] for v in velocities]
        plt.figure(figsize=(10, 6))
        plt.scatter(converted_resolutions + jitter_resolultion, framerates + jitter_framerate, c=colors, alpha=0.3) # edgecolor='k'

        # for scene, color in scene_colors.items():
        for speed, color in speed_colors.items():
            plt.scatter([], [], c=color, alpha=0.7, s=100, label=speeds_dict[speed])  # Dummy scatter for legend
        plt.legend(title='Speeds', fontsize=8)
        # plt.legend(title="Marker Size ~ Velocity", loc='upper right')

        plt.xlabel('Resolution (height in px)',  fontsize=15)
        plt.ylabel('Framerate (Hz)',  fontsize=15)
        x_values = [360, 480, 720, 864, 1080]
        evenly_spaced_x = range(len(x_values))

        # Set the x-ticks to the evenly spaced positions
        plt.xticks(evenly_spaced_x, x_values)
        # plt.xticks([360, 480, 720, 864, 1080])
        plt.yticks([i for i in range(30, 131, 10)])
        plt.title(f'{bitrate_mapping[bitrate]}', fontsize=15, color='black')
        plt.grid(True, c='lightgrey', linestyle='--')

        plt.tight_layout()
        # plt.text(0.08, 0.11, bitrate_mapping[bitrate], fontsize=15, color='black', transform=plt.gcf().transFigure,  # Transform coordinates to figure-relative
        #          ha="left", va="bottom") # darkgrey, black

        today = get_today()
        now = datetime.now()
        time_path = now.strftime("%Y-%m-%d-%H_%M")
        folder = f"imageoutput/{today}"
        os.makedirs(folder, exist_ok=True)
        if SAVE:
            plt.savefig(f"{folder}/{bitrate}-{time_path}.png", bbox_inches='tight', pad_inches=0.1)
        if SHOW:
            plt.show()
        # break


# Dont plot scene name, color represents velocity
if __name__ == "__main__":

    SAVE = True
    SHOW = False # True False
    
    # scene_colors = {path: f'C{i}' for i, path in enumerate(SCENES)}
    # scene_colors = {'bedroom': 'dodgerblue', # C0', 
    #                 'bistro': 'C1', 'crytek_sponza': 'C2', 
    #                 'gallery': 'orangered', # 'C3', 
    #                 'living_room': 'C4', 'lost_empire': 'C5', 'room': 'C6', 'suntemple': 'C7', 
    #                 'suntemplestatue': 'gold', #'C8', 
    #                 'sibenik': 'C9'}
    speeds_dict = {1: 'Slow', 2: 'Medium', 3: 'Fast'}
    speed_colors =  { 1: "gold", 2: "deepskyblue", 3: "salmon"}
    unique_paths = {'bedroom': 'Bedroom', 'bistro': 'Bistro', 'crytek_sponza': 'Crytek sponza', 'gallery': 'Gallery', 'living_room': 'Living room', 'lost_empire': 'Lost empire', 'room': 'Room', 'suntemple': 'Suntemple', 'suntemplestatue': 'Statue', 'sibenik': 'Sibenik'}
    # print(f'scene_colors {scene_colors}')
    res_mapping = {360:0, 480:1, 720:2, 864:3, 1080:4}
    bitrate_mapping = {500: '0.5 Mbps', 1000: '1 Mbps', 1500: '1.5 Mbps', 2000: '2 Mbps', 3000: '3Mbps', 4000: '4Mbps'}

    plot()
