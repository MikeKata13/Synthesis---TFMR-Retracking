import sys
import functions as fn
import numpy as np
import matplotlib.pyplot as plt



file_list=list()
with open('Valid_Names.txt', 'r') as file:
    for line in file:
        file_list.append(line.rstrip('\n'))

# Get the necessary variables from the needed file


points,pwr,time,altitude=fn.data_parsing(file_list[0])

# Import elevation map
elev_f='arcticdem_mosaic_500m_v3.0.tif'
elevation_array=fn.elevation_map(elev_f)
upper_quantile=np.quantile(elevation_array,0.75)

# Plot the elevations for checking
print(f'Minimum: {np.min(elevation_array)}')
print(f'Maximum: {np.max(elevation_array)}')
print(f'Upper Quantile: {upper_quantile}')
flat=elevation_array.flatten(order='C')
plt.plot(flat)
plt.show()
