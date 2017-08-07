import urllib
from pyproj import Proj
proj = urllib.urlopen('http://spatialreference.org/ref/sr-org/7483/proj4/').read()
shape_file = '/Volumes/Samsung USB/dev/shapefiles/zipcodesUS/mainlandUSzip.shp'
test_df = gpd.GeoDataFrame.from_file(shape_file)

test_df = test_df[['ZCTA5CE10', 'geometry', 'StateAbbr']]
nc_df = test_df[test_df.StateAbbr == 'NC']
nc_df.drop_duplicates('ZCTA5CE10', keep='first', inplace=True)
epsg = getEPSG_of_shapefile(shape_file)

# WGS 84
inProj = Proj(init = 'epsg:{}'.format(epsg))

# Web mercator 
outProj = Proj(init='epsg:3857')

proj_df = nc_df.to_crs(proj)
#proj_json = proj_df.to_json()
proj_df.to_file('/Users/thays/Desktop/geo_utils/NC_zips_3857.shp', driver='ESRI Shapefile')