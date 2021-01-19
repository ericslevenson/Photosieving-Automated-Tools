## Defaults
from pathlib import Path

# Main folder path
main_folder = Path(r"X:\E_Levenson\1Github\\")

# folder path containing xml camera files from Agisoft Metashape
camera_folder_xml = Path(r"X:\E_Levenson\1Github\cameras\xml")

# path to empty folder that will contain camera information in csv format
camera_folder_csv = Path(r"X:\E_Levenson\1Github\cameras\csv")

# folder path containing sub folders of images for each bar
bar_folder = Path(r"X:\E_Levenson\1Github\bars")

# csv file containing bar heights
barheights_path = Path(r"X:\E_Levenson\1Github\barheights.csv")

# Set maximum flying height (meters) to include in PebbleCounts
agl_threshold = 8

# Empty folder to copy images to run through PebbleCounts
highres_folder = Path(r"X:\E_Levenson\1Github\high_res_images")

# Camera specifications
focal_length_mm = 10.26
sensorH_mm = 8.8
sensorW_mm = 13.2
pixelsH = 3628
pixelsW = 5472

# Maximum grain size
maxgs = 2
