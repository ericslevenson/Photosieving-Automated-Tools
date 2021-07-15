# Parse xml outputs from Agisoft and create a master matrix of image labels,
    # lat, lon, and elevations.

# *** Imports ***
import sys
import os
import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# *** Inputs ***

# folder path containing xml camera files from Agisoft Metashape
camera_folder_xml = Path(r"X:\E_Levenson\1Github\cameras\xml")

# *** Outputs ***

# path to empty folder that will contain camera information in csv format
camera_folder_csv = Path(r"X:\E_Levenson\1Github\cameras\csv")

# *** Main ***

## Loop through each xml document in the camera folder to extract
    ## geographic information and resolution for each individual image and
    ## export to .csv of camera info still grouped by bar.
for filename in os.listdir(camera_folder_xml):
    file_path = Path(camera_folder_xml,filename)
    bar = filename.split('_')[0] # separate out just the bar name
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

    # combine lists into DataFrame
    cameras = {'ID':id, 'Label':label, 'Lat':y, 'Lon':x, "Elev":z, "AGL":agl, "Resolution":camera_resolution}
    camera_info = pd.DataFrame(cameras)
    # create new filename and write to csv
    new_filename = Path(str(bar) + '_cameras.csv')
    camera_info.to_csv(Path(camera_folder_csv,new_filename))
