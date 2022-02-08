from sqlalchemy import create_engine
db_string = "postgresql://localhost/era5"
db_connection = create_engine(db_string)

# check the connection
#c = db_connection.execute("SELECT UpdateGeometrySRID('era5','geometry',4326);")

#c = db_connection.execute("CREATE INDEX spatial_index_era5 ON era5 USING GIST (geometry);")
with db_connection.connect() as con:
    #res = con.execute("SELECT * from spatial_ref_sys;")
    res = con.execute("SELECT * FROM era5 WHERE ST_Distance( geometry, 'SRID=4326;POINT(-53.883 -25.604)' ) < 0.001;")

for r in res:
    print(r)
