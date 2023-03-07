import netCDF4
from lxml import etree
from shapely.geometry import Polygon, Point
from osgeo import gdal
import matplotlib.pyplot as plt

# Function to read and parse the kml file and store the polygon coordinates
def read_kml(kml_file):
    tree = etree.parse(kml_file)
    root = tree.getroot()
    namespace = '{http://www.opengis.net/kml/2.2}'
    placemarks = root.findall(f'.//{namespace}Placemark')
    polygon_coords = list()
    for placemark in placemarks:
        polygon = placemark.find(f'.//{namespace}Polygon')
        if polygon is not None:
            coord_text = polygon.find(f'.//{namespace}coordinates').text
            coords = [tuple(map(float, coord.split(',')))[:2] for coord in coord_text.strip().split(' ')]
            polygon_coords.append(coords)
    return polygon_coords

# Function to check if a point is in the polygon
def is_point_in_mask(polygon_coords, point):
    polygon = Polygon(polygon_coords[0])
    return polygon.contains(Point(point))

def data_parsing(file):
    points=list()
    with netCDF4.Dataset(file, 'r') as nc:
        lon = nc.variables['lon_20_ku'][:]
        lat = nc.variables['lat_20_ku'][:]
        pwr=nc.variables['pwr_waveform_20_ku'][:]
        time=nc.variables['time_20_ku'][:]
        altitude=nc.variables['alt_20_ku'][:]
        altitude_rate=nc.variables['orb_alt_rate_20_ku'][:]
        for latitude, longitude in zip(lat,lon):
            points.append([latitude, longitude])
    return points, pwr, time, altitude

def elevation_map(file):    
    dataset=gdal.Open(file)
    # We store in different variables the different chromatic channels
    band1 = dataset.GetRasterBand(1) # Monochrome channel
    b1 = band1.ReadAsArray()
    # Cropping to get only Greenland
    b1=b1[8500:15000,6500:10000]
    f = plt.figure()
    plt.imshow(b1,cmap='viridis')
    plt.colorbar()
    plt.title('Elevation Map')
    saved_image=plt.savefig(f'Elevation_Image_{file}.png')
    plt.close()
    return b1

def elevation_map2(file):
    dataset = gdal.Open(file)

    # Get the geolocation information
    transform = dataset.GetGeoTransform()
    x_origin = transform[0]
    y_origin = transform[3]
    pixel_width = transform[1]
    pixel_height = transform[5]

    # Get the elevation values as a numpy array
    band = dataset.GetRasterBand(1)
    elevation_array = band.ReadAsArray()

    # Close the file
    dataset = None

    # Plot the elevation map as an image
    plt.imshow(elevation_array, cmap='hot', interpolation='nearest')
    plt.show()
    # Loop through the elevation array and print the geolocation and elevation values (this can be used later for creating the grid)
    rows, cols = elevation_array.shape
    for row in range(rows):
        for col in range(cols):
            elevation = elevation_array[row][col]
            x = x_origin + col * pixel_width
            y = y_origin + row * pixel_height
            #print(f"Geolocation: ({x}, {y}), Elevation: {elevation}")
