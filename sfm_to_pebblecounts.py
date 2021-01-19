# Imports
import shutil, os, shutil, sys, csv, re
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from pathlib import Path
from config import *

## Task 1: Rename each image to include its bar name. This also gives each
    ## image a unique name.
bar_list = [] # create empty list for bar names
for filename in os.listdir(bar_folder):
    bar = str(filename)
    bar_list.append(bar)
    folder_path = Path(bar_folder,filename)
    for imagename in os.listdir(folder_path):
        image_path = Path(folder_path,imagename)
        new_imagename = bar+'_'+imagename
        new_imagepath = Path(folder_path,new_imagename)
        shutil.move(image_path, new_imagepath)

## Task 2: Get information on bar heights. This will be used to
    ## calculate image resolution
barheights = pd.read_csv(barheights_path) # Read in barheights .csv and create dataframe
barheights['Bar Name'] = barheights['Bar Name'].apply(str) # convert bar names to string

## Task 3: Loop through each xml document in the camera folder to extract
    ## geographic information and resolution for each individual image and
    ## export to .csv of camera info still grouped by bar.
for filename in os.listdir(camera_folder_xml):
    file_path = Path(camera_folder_xml,filename)
    bar = filename.split('_')[0] # separate out just the bar name
    bar_list.append(bar)
    # Parse information from xml format and create lists
    tree = ET.parse(file_path)
    root = tree.getroot()
    id, label, x, y, z = [], [], [], [], []
    for camera in root.iter('camera'):
        id1 = camera.get('id')
        id.append(id1)
        label1 = camera.get('label')
        label1 = str(bar + '_' + label1)
        label.append(label1)
        x1 = camera.find('reference').get('x')
        x.append(x1)
        y1 = camera.find('reference').get('y')
        y.append(y1)
        z1 = camera.find('reference').get('z')
        z.append(z1)

    # Get bar heights to calculate above ground level
    barheight = float(barheights.loc[barheights['Bar Name']==bar, 'Height']) # get the height based on matching bar name
    agl, agl1, agl2, agl3 = [], [], [], []
    for height in z:
        agl1 = float(height)
        agl2.append(agl1)
    for height in agl2:
        agl3 = height - barheight
        if agl3 < 1:
            agl3 = 1 # This is optional, I knew that I didn't fly lower than 1 meter so I set a lower threshold.
        agl.append(agl3)

    # Calculate image Resolution using camera characteristics
    fovH_m, fovW_m, x_res, y_res, camera_resolution1, camera_resolution = [], [], [], [], [], []
    for  flyingheight in agl:
        fovH_m = (sensorH_mm/focal_length_mm)*flyingheight
        fovW_m = (sensorW_mm/focal_length_mm)*flyingheight
        x_res, y_res = np.round(fovH_m*1000/pixelsH, 4), np.round(fovW_m*1000/pixelsW, 4)
        camera_resolution1 = np.round(np.mean([x_res, y_res]), 4)
        camera_resolution.append(camera_resolution1)

    # combine lists into DataFrame
    cameras = {'ID':id, 'Label':label, 'Lat':y, 'Lon':x, "Elev":z, "AGL":agl, "Resolution":camera_resolution}
    camera_info = pd.DataFrame(cameras)
    # create new filename and write to csv
    new_filename = Path(str(bar) + '_cameras.csv')
    camera_info.to_csv(Path(camera_folder_csv,new_filename))

## Task 4: Subset high resolution images from each bar's .csv of camera
    ## information and combine into one DataFrame
high_res_images = pd.DataFrame({"Unnamed: 0":[], # empty dataframe
                                "ID":[],
                                "Label":[],
                                "Lat":[],
                                "Lon":[],
                                "Elev":[],
                                "AGL":[],
                                "Resolution":[]})

# Loop through .csv files
for filename in os.listdir(camera_folder_csv):
    file_path = Path(camera_folder_csv,filename)
    csv = pd.read_csv(file_path)
    keepers = csv[csv.AGL <= agl_threshold] # create dataframe of low altitude images from this bar
    high_res_images = high_res_images.append(keepers, ignore_index=True)
high_res_images.Label = high_res_images.Label.astype(str) # convert labels to strings

## Task 5: Copy every image destined for PebbleCounts from its bar folder into
    ## one folder designated for high resolution images
for folder in os.listdir(bar_folder):
    folder_path = Path(bar_folder,folder)
    # Loop through image files
    for filename in os.listdir(folder_path):
        label = str(filename.split('.')[0]) # Separate out the label
        if high_res_images['Label'].str.contains(label).any(): # check if label is one of the low altitude images
            file_path = Path(folder_path,filename) # if so, define the file path
            new_filepath = Path(highres_folder,filename) # also create the new file path
            shutil.copyfile(file_path, new_filepath) # copy images to new file path. If you are brave you could save space and  move these images instead of copying.

## Task 6: Create PebbleCounts commandline arguments and combine into a .csv
high_res_images['Label'] = high_res_images['Label'].apply(str)
high_res_images['Resolution'] = high_res_images['Resolution'].apply(float)
command_list = []
# Loop through image files to create file path
for filename in os.listdir(highres_folder):
    label = str(filename.split('.')[0])
    resolution = high_res_images.loc[high_res_images['Label']==label, ['Resolution']]
    resolution_val = float(resolution.iloc[0])
    command = r'python PebbleCounts.py -im ' + str(highres_folder) + "\\" + filename + r' -ortho n -maxGS ' + str(maxgs) + r' -subset y -input_resolution ' + str(resolution_val)
    command_list.append(command)
command_list = pd.DataFrame(command_list)
commandlinepath = Path(str(main_folder),r"commandline.csv")
command_list.to_csv(commandlinepath)
