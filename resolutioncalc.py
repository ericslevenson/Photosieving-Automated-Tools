## Calculate the resolution (mm/pixel) for each image using the camera
   ## elevation, the surface elevation, and the camera specs.
# Imports
import os
import pandas as pd
import numpy as np
from pathlib import Path


# *** Inputs ***

# path to folder that contains camera information in csv format
camera_folder = Path(r"X:\E_Levenson\1Github\cameras\csv")

# folder containing .csv files with surface elevations at each point.
barfolder = Path(r"C:\Users\elevens2\sandy_python\cameras\point_elevations") 
# Header for the column of surface elevations
surface_elev = 'RASTERVALU'

# Camera specifications
focal_length_mm = 10.26
sensorH_mm = 8.8
sensorW_mm = 13.2
pixelsH = 3628
pixelsW = 5472

# messing with rescalc
x = ((sensorH_mm/focal_length_mm)*1000)/pixelsH
y = ((sensorW_mm/focal_length_mm)*1000)/pixelsW
print(np.mean([x, y]))

# *** Outputs ***

# csv master matrix
master_matrix = Path(r"C:\Users\elevens2\sandy_python\master_matrix.csv")

# *** Main ***

# Create dataframe for image labels and bar elevations
labels, barh = [],[]
for filename in os.listdir(barfolder):
    file_path = Path(barfolder,filename)
    csv = pd.read_csv(file_path)
    labels.extend(csv['Label'].tolist())
    barh.extend(csv[surface_elev]) 
bars = {'label':labels, 'barheight':barh}
bars = pd.DataFrame(bars)

# Combine all images from their bar .csvs into one dataframe
labels2, z, lat, lon = [],[], [], []
for filename in os.listdir(camera_folder):
    file_path = Path(camera_folder,filename)
    csv = pd.read_csv(file_path)
    labels2.extend(csv['Label'].tolist())
    z.extend(csv['Elev'].tolist())
    lat.extend(csv['Lat'].tolist())
    lon.extend(csv['Lon'].tolist())
cameras = {'label':labels2, 'z':z, 'lat':lat, 'lon':lon}
cameras = pd.DataFrame(cameras)

# Combine matrices
imageinfo = pd.merge(bars, cameras, how='inner', on='label') 
# Calculate camera altitude above ground level
imageinfo['agl'] = imageinfo['z']-imageinfo['barheight'] 
# Calculate image resolution
x = ((sensorH_mm/focal_length_mm)*1000)/pixelsH
y = ((sensorW_mm/focal_length_mm)*1000)/pixelsW
rescoefficient = np.round(np.mean([x,y]), 4)
imageinfo['resolution'] = imageinfo['agl']*rescoefficient

# Export to .csv
imageinfo.to_csv(master_matrix)




