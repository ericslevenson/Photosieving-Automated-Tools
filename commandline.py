# This script is designed to create command line inputs for every high res
    # image in a .csv file

# *** Imports ***
import os, csv
from pathlib import Path
import pandas as pd

# *** Inputs ***

# .csv file of camera information (including label and resolution)
master_matrix = Path(r"C:\Users\elevens2\sandy_python\master_matrix.csv")
# Folder containing high resolution image files
highres_folder = r"X:\E_Levenson\1Github\high_res_images"
# Maximum grain-size
maxGS = 2

# *** Outputs ***
# Path to .csv file of commandline arguments
commandline = Path(r"C:\Users\elevens2\sandy_python\commandline.csv")

# *** Main ***

# Create PebbleCounts commandline arguments and combine into a .csv
high_res_images = pd.read_csv(master_matrix)
high_res_images['Label'] = high_res_images['Label'].apply(str)
high_res_images['Resolution'] = high_res_images['Resolution'].apply(float)
command_list = []
# Loop through image files to create file path
for filename in os.listdir(highres_folder):
    label = str(filename.split('.')[0])
    resolution = high_res_images.loc[high_res_images['Label']==label, ['Resolution']]
    resolution_val = float(resolution.iloc[0])
    command = r'python PebbleCounts.py -im ' + str(highres_folder) + "\\" + filename + r' -ortho n -maxGS ' + str(maxGS) + r' -subset y -input_resolution ' + str(resolution_val)
    command_list.append(command)
command_list = pd.DataFrame(command_list)
# Export to csv
command_list.to_csv(commandline)