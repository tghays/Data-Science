import os

db_name = 'db_name'
host = 'host.host.us-east-1.rds.amazonaws.com'
port = '5432'
username = 'username'
password = 'password'
shape_path = '/Users/thays/Desktop/Geodata/zipcodesUS/US_zcta_zip/US_zcta_zip.shp'

os.system("""ogr2ogr -overwrite -progress -f PostgreSQL PG:"dbname={0} host={1} port={2} user={3} password={4}" {5} -nln geospatial_data.zcta_shape""".format(db_name, host, port, username, password, shape_path))