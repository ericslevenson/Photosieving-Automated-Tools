## This script renames every image to include the associated bar name.


# *** Imports ***
import shutil
import os
from pathlib import Path


# *** Inputs ***
# The folder path should contain subfolders named for individual bars. These
#   subfolders should contain the image files associated with that bar.

folder_path = r"X:\E_Levenson\1Github\bars\\"

# *** Main ***

# Create a list of bar names based on folder labels
bar_list = []
folder = Path(folder_path)
for filename in os.listdir(folder_path):
    bar_list.append(filename)

# Rename image files to include the bar name
for bar in bar_list:
    bar_path = Path(folder,bar)
    # Loop through image files
    for filename in os.listdir(bar_path):
        file_path = Path(bar_path,filename) # define original file path
        new_filename = bar+'_'+filename # define new file name
        new_filepath = Path(bar_path,new_filename) # define new file path
        shutil.move(file_path, new_filepath) # replace file names