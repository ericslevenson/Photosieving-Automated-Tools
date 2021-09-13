# Supply a maximum image resolution to include for photosieving, and this 
    # script will move the appropriate images to a single high resolution
    # image folder, and subset their information in the master matrix.

# *** Imports ***
import shutil
import csv
import os
from pathlib import Path
import pandas as pd

# *** Inputs ***

# What's the maximum resolution you want to include for photosieving? This will 
# determine the smallest measurable grain size.
max_resolution = 0.707
# Alternatively you can use a maximum AGL by changing line FIXME
max_AGL = 4
# Matrix of camera information (likely the output of resolutioncalc.py)
camerainfo = Path(r"C:\Users\elevens2\sandy_python\master_matrix.csv")
# Folder containing subfolders named for individual bars. These subfolders
#   should contain the image files associated with that bar.
bar_folder = Path(r"X:\E_Levenson\1Github\bars\\")

# *** Outputs ***

# Folder that will hold the high resolution image files
highres_folder = Path(r"X:\E_Levenson\1Github\high_res_images")
# csv master matrix
master_matrix = Path(r"C:\Users\elevens2\sandy_python\master_matrix.csv")

# *** Main ***

## Subset high resolution images from camera information
csv = pd.read_csv(camerainfo)
matrix = csv[csv.resolution <= max_resolution]
matrix.Label = master_matrix.Label.astype(str) # convert labels to strings
matrix.to_csv(master_matrix)

# Copy every high resolution image into one folder
for folder in os.listdir(bar_folder):
    folder_path = Path(bar_folder,folder)
    # Loop through image files
    for filename in os.listdir(folder_path):
        label = str(filename.split('.')[0]) # Separate out the label
        if matrix['Label'].str.contains(label).any(): # check if label is one of the low altitude images
            file_path = Path(folder_path,filename) # if so, define the file path
            new_filepath = Path(highres_folder,filename) # also create the new file path
            shutil.copyfile(file_path, new_filepath) # copy images to new file path. If you are brave you could save space and  move these images instead of copying.