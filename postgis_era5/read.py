from sqlalchemy import create_engine
db_string = "postgresql://localhost/era5"
db_connection = create_engine(db_string)

with db_connection.connect() as con:
    #res = con.execute("SELECT * from spatial_ref_sys;")
    #res = con.execute("SELECT * FROM era5 WHERE ST_Distance( geometry, 'SRID=4326;POINT(-4.960 -75.266)' ) < 0.01;")
    res = con.execute("SELECT * FROM era5 WHERE time >= '2021-05-10' AND time <  '2021-05-20' AND ST_Distance( geometry, 'SRID=4326;POINT(-4.960 -75.266)' ) < 0.01;;")

for r in res:
    print(r)
