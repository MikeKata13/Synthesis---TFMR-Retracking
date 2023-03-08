
from libraries import *


# Import the file
file_list=list()
with open('Valid_Names.txt', 'r') as file:
    for line in file:
        file_list.append(line.rstrip('\n'))

# Get the necessary variables from the needed file
points,pwr,time,altitude=fn.data_parsing(file_list[0])

# Calculate the radius of the earth for every point in the "points" variable (latitude and longitude)
print(points[0])


# Import elevation map and get the elevations, the latitude and the longitude
dem_file='arcticdem_mosaic_500m_v3.0.tif'
elevation_array,x_grid,y_grid,lon_DEM_grid,lat_DEM_grid=fn.elevation_map(dem_file)
upper_quantile=np.quantile(elevation_array,0.75)

# Plot the elevations for checking
min_elevation=np.around(np.min(elevation_array))
max_elevation=np.around(np.max(elevation_array))
print(f'Minimum: {min_elevation} meters')
print(f'Maximum: {max_elevation} meters')
print(f'Upper Quantile: {round(upper_quantile,2)} meters')
flattened_elevation=elevation_array.flatten(order='C')
plt.plot(flattened_elevation)
#plt.show()

#max_index=elevation_array.index(np.max(elevation_array))
#print(max_index)
print(f'Earth Radius at point {points[-1]} is {fn.earth_radius(points[-1])} meters.')
