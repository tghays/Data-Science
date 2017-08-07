from osgeo import ogr, gdal

def getExtents(shpfn):
    inShp = shpfn
    inDriver = ogr.GetDriverByName(driverName)
    inDataSource = inDriver.Open(inShp)
    inLayer = inDataSource.GetLayer()
    working_extent = inLayer.GetExtent()
    x = [working_extent[0], working_extent[1]]
    y = [working_extent[2], working_extent[3]]
    center = (sum(x) / len(x), sum(y) / len(y))
    center_x, center_y = center[0], center[1]
    x_frame, y_frame = abs(x[0] - x[1]) * (-0.025), abs(y[0] - y[1]) * (0.025)
    frame_extent = [x[0] + x_frame, x[1] - x_frame, y[0] - y_frame, y[1] + y_frame]
    return (frame_extent, working_extent, (center_x, center_y))