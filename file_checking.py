import netCDF4
import os
from lxml import etree
from shapely.geometry import Polygon, Point
from functions import read_kml, is_point_in_mask

# Open, parse the files and create the polygon mask
kml_file = 'Greenland_LRM_Mask.kml'
polygon_coords = read_kml(kml_file)
#nc_file = input('Write the name of the input file: ') : Keep this line if you only want to check the files by name

# Check if the track overlaps with the mask.
folder_path = input('Enter the folder path: ') 

file_list = os.listdir(folder_path)
nc_files=list()
for i in file_list:
    if i.endswith('.nc'):
        nc_files.append(i)
folder_items_number=len(nc_files)
valid_nc_files=list()
steps=0
for file in nc_files:
    file_path = os.path.join(folder_path, file)
    
    def processing(path):
        with netCDF4.Dataset(path, 'r') as nc:
            lon = nc.variables['lon_20_ku'][:]
            lat = nc.variables['lat_20_ku'][:]
            pwr=nc.variables['pwr_waveform_20_ku'][:]

        for latitude, longitude in zip(lat,lon):
                points = [(latitude, longitude)]
        
        # Check if there are points from the file inside the mask (If the track goes through the mask)
        for point in points:
            if is_point_in_mask(polygon_coords, point):
                valid_nc_files.append(path)
        return valid_nc_files
    valid=processing(file_path)
    steps+=1
    print(f'Progress: {steps}/{folder_items_number}')
print(f'The number of the tracks that go through the mask is: {len(valid)}')
if valid != 0:
    print(valid)
# Save the names of the valid files into a .txt file.
valid_file_names=open('Valid_Names.txt','w')
for name in valid:
    valid_file_names.write(name+'\n')
valid_file_names.close()

