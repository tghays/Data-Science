import sys, os, imp
from osgeo import ogr, gdal
import matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Proj


def createMap():
    shpfn = workingDir + 'states/' + 'USA_wgs84' + '.shp'
    extOutput = getExtents(shpfn)
    center_x = extOutput[2][0]
    center_y = extOutput[2][1]
    frame_extent = extOutput[0]
    working_extent = extOutput[1]
    lon_0, lat_0 = (center_x, center_y)
    llcrnrlon, urcrnrlon = (frame_extent[0], frame_extent[1])
    llcrnrlat, urcrnrlat = (frame_extent[2], frame_extent[3])

    # Create map instance
    m = Basemap(epsg=4269, \
                #width=exts[0],
                #width=12000000,
                #height= exts[1] + exts[1]*.1, 
                #height=8000000,
                lon_0 = lon_0, lat_0 = lat_0 + lat_0*.05, \
                resolution='l',
                projection='lcc')#, \
                #llcrnrlon = llcrnrlon, llcrnrlat = llcrnrlat,\
                #urcrnrlon = urcrnrlon, urcrnrlat = urcrnrlat)
            
def map_limits(m):
    llcrnrlon = min(m.boundarylons)
    urcrnrlon = max(m.boundarylons)
    llcrnrlat = min(m.boundarylats)
    urcrnrlat = max(m.boundarylats)
    return llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat