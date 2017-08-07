from sqlalchemy import create_engine
username = 'username'
password = 'password'
db_name = 'db_name'
port = '5432'
connection = 'db_name.db_name.us-east-1.rds.amazonaws.com'
engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(username,password,connection,port,db_name))
connection = engine.connect()

sql = "SELECT ogc_fid, zcta, wkb_geometry FROM geospatial_data.zcta_shape WHERE stateabbr = 'NC'"
test_df = gpd.read_postgis(sql, connection, geom_col='wkb_geometry')