# Photosieving-Workflow

## Overview and objectives
Photosieving techniques for measuring sediment grain sizes from images presents the opportunity to observe the spatial patterns in grain size distributions with such expansive coverage that local and bar scale patterns can be examined across entire river segments. The objective here is to use nadir images of gravel bars collected in the field (in this case from a UAV) and create grain size distributions that are attached to their point location within the river system.  The challenge of surveying and georeferencing camera locations is addressed elsewhere through work on direct georeferencing of camera locations using Structure from Motion in Agisoft Metashape (See Carbonneau and Dietrich). The sfm_to_pebblecounts.py script builds on that work by addressing the central challenge of efficiently processing the combination of the outputs of the SfM process and the original images in preparation for photosieving. PebbleCounts, produced by Ben Purinton, is chosen as a photosieving technique due to its applicability to the coarse grain sizes of the study site on Oregon's Sandy River. The GSD.py script calculates grain size percentiles and attaches them to their locational information, which can easily be imported into a GIS. Details for the specific tasks of each of these scripts are included below.

## Inputs and outcomes
The inputs to this workflow include are listed below. Users can follow the organization of the example inputs given in this repository:\
(1) An image folder containing subfolders for each gravel bar. These subfolders should be named with the bar's given label and they should contain all of the original images    that were the inputs to the SfM workflow. (see bars folder) This automation will filter out the images that should not be included in photosieving based on a flying height     threshold.\
(2) A folder containing the .xml documents of camera information for each bar. Each file should follow the naming convention: "BARNAME_cameras.xml" (see cameras//xml folder)\
(3) An empty folder that will hold the .csv outputs of the camera information (see cameras//csv foler)\
(4) A .csv containing a column for the bar label and a column for its elevation. In the example, the elevations were calculated by sampling the DEM outputs of the SfM. (see         barheights.csv)\
(5) Empty folder folder that will hold copies of the images that are destined for photosieving. (see high_res_images folder)\
(6) Update the config.py script to include file paths to all of these folders, along with camera specifications and flying height threshold.\

The outcomes include:\
(1) .csv files for each bar of image latitude, longitude, elevevation, altitude above ground level, and image resolution (mm/pixel).\
(2) Renamed images that include their bar name in the file name.\
(3) A folder containing high resolution images from every bar.\
(4) A .csv containing the geographic and resolution information for these high resolution images.\
(5) A .csv of unique PebbleCounts commandline arguments for each image.\
(6) A .csv of grain size distributions from PebbleCounts attached to the correct geographic information.
 

## Background information
I need to mention the organization of the river and its practical implications for this workflow. Every image and therefore every grain size distribution is taken over a gravel bar, which means it is part of a group along with the other images that are taken over the same bar. Following image collection, the raw images were grouped into folders based on their bar membership (see bar folder in the repository), and each bar folder was the input for the SfM project in Agisoft Metashape. This organization by bar is reflected in the camera xml outputs from SfM along with the folder structure of the images, which means this organization plays an integral role in linking the geographic information sourced from the .xml documents with the actual image.

means that the camera xml documents and image folders are each grouped by their gravel bar. This repository includes 3 of the 37 gravel bars surveyed as part of this project named in downstream order (A, B, C...). This is important to understand, since it plays an integral role in linking the geographic information sourced from the .xml documents with the actual image.

## Sfm_to_Pebblecounts
The objectives of this script are to:\
  1: Rename every image to include its bar label. This also gives every image a unique name.\
  2: Get information on each bar height from the DEM created through the SfM process.\
  3: Extract geographic information from the Agisoft Metashape .xml documents and calculate image resolutions.\
  4: Subset the high resolution images to be included in photosieving and copy them into one folder.\
  5: Create commandline arguments for every image and export to a .csv.


This repository addresses a central challenge for the application of photosieving techniques to river segments, which is efficiently pre-processing the images for a photosieving method. 

In this case I use PebbleCounts produced by Ben Purinton as a photosieving technique, which requires a specific commandline argument for each image that includes its file location and image resolution. The code presented here automates the process of 
extracting information on each image's location and resolution in order to pre-process 

Pebblecounts requires a unique commandline argument for each image that includes its file location and image resolution
