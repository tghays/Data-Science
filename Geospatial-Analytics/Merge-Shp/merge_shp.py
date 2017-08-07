import sys, os, imp
from osgeo import ogr, gdal
import matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Proj

workingDir = '/media/tyler/Samsung USB/dev/shapefiles/'
driverName = 'ESRI Shapefile'

def mergeShps(states):
    '''
    Merges multiple state shapefiles into a single state shapefile

    Syntax:
    mergeShps(['NC', 'SC', 'GA'])
    '''

    geometryType = ogr.wkbPolygon
    outputMergefn = workingDir + ''.join(states) + '.shp'
    out_driver = ogr.GetDriverByName( driverName )
    states_paths = [(workingDir + 'states/' + x + '.shp') for x in states]

    #Check if the output file exists, delete if so
    if os.path.exists(outputMergefn):
        out_driver.DeleteDataSource(outputMergefn)

    # Set output file
    out_ds = out_driver.CreateDataSource(outputMergefn)
    out_layer = out_ds.CreateLayer(outputMergefn, geom_type=geometryType)

    for stateFile in states_paths:
        ds = ogr.Open(stateFile)
        lyr = ds.GetLayer()
        for feat in lyr:
            out_feat = ogr.Feature(out_layer.GetLayerDefn())
            out_feat.SetGeometry(feat.GetGeometryRef().Clone())
            out_layer.CreateFeature(out_feat)
            out_feat = None
            out_layer.SyncToDisk()

    shpfn = outputMergefn
    return shpfn