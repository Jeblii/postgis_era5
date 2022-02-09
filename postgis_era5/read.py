import statistics
from typing import List

import sqlalchemy
from geoalchemy2 import Geometry
from sqlalchemy import MetaData, Table, bindparam, create_engine, DateTime, Column, Float, select
from sqlalchemy.sql import text

from postgis_era5.types import WGS84Point

db_string = "postgresql://localhost/era5"
db_connection = create_engine(db_string)

era5_table = Table(
    'era5',
    MetaData(),
    Column('time', DateTime),
    Column('u10_min', Float),
    Column('u10_max', Float),
    Column('u10_mean', Float),
    Column('v10_min', Float),
    Column('v10_max', Float),
    Column('v10_mean', Float),
    Column('d2m_min', Float),
    Column('d2m_max', Float),
    Column('d2m_mean', Float),
    Column('t2m_min', Float),
    Column('t2m_max', Float),
    Column('t2m_mean', Float),
    Column('lai_hv_min', Float),
    Column('lai_hv_max', Float),
    Column('lai_hv_mean', Float),
    Column('pev_min', Float),
    Column('pev_max', Float),
    Column('pev_mean', Float),
    Column('slhf_min', Float),
    Column('slhf_max', Float),
    Column('slhf_mean', Float),
    Column('ssr_min', Float),
    Column('ssr_max', Float),
    Column('ssr_mean', Float),
    Column('str_min', Float),
    Column('str_max', Float),
    Column('str_mean', Float),
    Column('ssh_min', Float),
    Column('ssh_max', Float),
    Column('ssh_mean', Float),
    Column('e_min', Float),
    Column('e_max', Float),
    Column('e_mean', Float),
    Column('tp_min', Float),
    Column('tp_max', Float),
    Column('tp_mean', Float),
    Column('geometry', Geometry('POINT'))
)

print(era5_table)

class PSQLInterface:

    engine: sqlalchemy.engine.base.Engine

    def __init__(self, engine: sqlalchemy.engine.base.Engine) -> None:
        self.engine = engine

    def check_connection(self) -> None:
        with self.engine.connect() as conn:
            res = conn.execute(
                """
                SELECT 1;
                """
            ).fetchall()
            if res != [(1,)]:
                raise Exception(
                    f"unexpected value when running the health check, expected [(1,)] but found {repr(res)}, "
                )

    def get_closest_point(self, location: WGS84Point):
        # TODO(Jeffrey Tsang) this only works for point. Not yet tested for other types of geometry for behaviour. See also https://postgis.net/workshops/postgis-intro/knn.html
        wkt_text = f"SRID=4326;POINT({location.longitude} {location.latitude})"
        query = text(
            """
                SELECT ST_AsText(geometry), t2m_min FROM era5
                WHERE EXTRACT(MONTH FROM time) = 5 
                ORDER BY geometry::geometry <-> ST_GeomFromText(:wkt)::geometry
                LIMIT 1;
                """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, wkt=wkt_text).fetchall()
        return res[0]['st_astext']

    def retrieve_norm(
        self, var: str, month: int, location: WGS84Point, year_range: int = 10
    ):

        closest_point = self.get_closest_point(location=location)
        closest_point = f'SRID=4326;{closest_point}'
        query = text(
            """
            SELECT AVG(t2m_min), AVG(t2m_max), ST_AsText(geometry) FROM era5 
            WHERE EXTRACT(MONTH FROM time) = :month
            AND ST_DWithin(geometry, :closest_geo, 0)
            GROUP BY geometry;
            """
            #AND ST_DWithin(geometry, 'SRID=3857;:z', 0);
            # kolom naam kan niet echt een variabel zijn. query builder api gebruiken.
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, month=month, closest_geo=closest_point).fetchall()
        return res

    def retrieve_historical_month_year(
        self, var: str, month: int, location: WGS84Point, year=int
    ):
        query = text(
            """
            SELECT AVG(t2m_min) 
            FROM era5 
            WHERE EXTRACT(MONTH FROM time) = :y 
            AND EXTRACT(YEAR FROM time) = :z;
            """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, y=month, z=year).fetchall()
        return res


db = PSQLInterface(db_connection)
db.check_connection()

# s = select(era5_table.c.t2min)
# with db_connection.connect() as conn:
#     result = conn.execute(s)
#     for row in result:
#         print(row)
# res = db.get_closest_point(WGS84Point(latitude=-22.804, longitude=-54.383))
# print(res)
res = db.retrieve_norm(var="t2m_min", month=5, location=WGS84Point(latitude=-22.804, longitude=-54.383))
print(res)
# res = db.retrieve_historical_month_year(var='t2m_min', month=5, year=2020)
# print(res)

# with db_connection.connect() as con:
#     # res = con.execute("SELECT * from spatial_ref_sys;")
#     # res = con.execute("SELECT * FROM era5 WHERE ST_Distance( geometry, 'SRID=4326;POINT(-4.960 -75.266)' ) < 0.01;")
#     # res = con.execute(
#     #     "SELECT ST_AsText(geometry) FROM era5 WHERE time >= '2011-05-10' AND time <  '2011-05-20' AND ST_Distance( geometry, 'SRID=4326;POINT(-54.383 -22.804)' ) < 0.01;"
#     # )


#     # get closest point
#     res = con.execute(
#         """
#         SELECT ST_AsText(geometry) FROM era5
#         WHERE EXTRACT(MONTH FROM time) = 5
#         ORDER BY geometry <-> ST_GeomFromText('SRID=4326;POINT(-54.383 -22.804)')
#         LIMIT 1;
#         """
#     ).fetchall()

#     print(res)


# result = [r[0] for r in res]
# print(len(result))
# print(statistics.mean(result))
