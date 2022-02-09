from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sqlalchemy
from typing import List
import statistics
from sqlalchemy import bindparam
import statistics
from postgis_era5.types import WGS84Point

db_string = "postgresql://localhost/era5"
db_connection = create_engine(db_string)


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
        wkt_text = f"SRID=4326;POINT({location.longitude} {location.latitude})"
        query = text(
            """
                SELECT ST_AsText(geometry) FROM era5
                WHERE EXTRACT(MONTH FROM time) = 5 
                ORDER BY geometry <-> ST_GeomFromText(:wkt)
                LIMIT 1;
                """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, wkt=wkt_text).fetchall()
        return res

    def retrieve_norm(
        self, var: str, month: int, location: WGS84Point, time_period: int = 10
    ):
        query = text(
            """
            SELECT :x FROM era5 WHERE EXTRACT(MONTH FROM time) = :y;
            """
        )
        query = query.bindparams(
            bindparam("x", type_=sqlalchemy.String),
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, x=var, y=month).fetchall()
        return res

    def retrieve_historical_month_year(
        self, var: str, month: int, location: WGS84Point, year=int
    ):
        query = text(
            """
            SELECT AVG(t2m_min) FROM era5 WHERE EXTRACT(MONTH FROM time) = :y AND EXTRACT(YEAR FROM time) = :z;
            """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, y=month, z=year).fetchall()
        return res


db = PSQLInterface(db_connection)
db.check_connection()
res = db.get_closest_point(WGS84Point(latitude=-22.804, longitude=-54.383))
print(res)
# res = db.retrieve_norm(var='t2m_min', month=5)
# print(res)
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
