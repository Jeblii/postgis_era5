from ast import parse
import statistics
from typing import List

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from postgis_era5.types import WGS84Point
from postgis_era5.parsing import parse_daily_norm

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
        # TODO(Jeffrey Tsang) this only works for point. Not yet tested for other types of geometry for behaviour. See also https://postgis.net/workshops/postgis-intro/knn.html
        wkt_text = f"SRID=4326;POINT({location.longitude} {location.latitude})"
        query = text(
            """
            SELECT ST_AsText(geometry) FROM era5
            WHERE EXTRACT(MONTH FROM time) = 5 
            ORDER BY geometry::geometry <-> ST_GeomFromText(:wkt)::geometry
            LIMIT 1;
            """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, wkt=wkt_text).fetchall()
        return res[0]["st_astext"]

    def retrieve_norm(
        self, var: str, month: int, location: WGS84Point, year_range: int = 10
    ):

        closest_point = self.get_closest_point(location=location)
        closest_point = f"SRID=4326;{closest_point}"
        query = text(
            """
            SELECT 
            ST_AsText(geometry) AS "geometry",
            EXTRACT(DAY FROM time) AS "day",
            EXTRACT(MONTH FROM time) AS "month",
            AVG(t2m_min) AS "t2m_min", 
            AVG(t2m_mean) AS "t2m_mean",
            AVG(t2m_max) AS "t2m_max",
            AVG(d2m_min) AS "d2m_min", 
            AVG(d2m_mean) AS "d2m_mean",
            AVG(d2m_max) AS "d2m_max",
            AVG(u10_min) AS "u10_min", 
            AVG(u10_mean) AS "u10_mean",
            AVG(u10_max) AS "u10_max",
            AVG(v10_min) AS "v10_min", 
            AVG(v10_mean) AS "v10_mean",
            AVG(v10_max) AS "v10_max",
            AVG(lai_hv_min) AS "lai_hv_min", 
            AVG(lai_hv_mean) AS "lai_hv_mean",
            AVG(lai_hv_max) AS "lai_hv_max",
            AVG(pev_min) AS "pev_min", 
            AVG(pev_mean) AS "pev_mean",
            AVG(pev_max) AS "pev_max",
            AVG(slhf_min) AS "slhf_min", 
            AVG(slhf_mean) AS "slhf_mean",
            AVG(slhf_max) AS "slhf_max",
            AVG(ssr_min) AS "ssr_min", 
            AVG(ssr_mean) AS "ssr_mean",
            AVG(ssr_max) AS "ssr_max",
            AVG(str_min) AS "str_min", 
            AVG(str_mean) AS "str_mean",
            AVG(str_max) AS "str_max",
            AVG(sshf_min) AS "sshf_min", 
            AVG(sshf_mean) AS "sshf_mean",
            AVG(sshf_max) AS "sshf_max",
            AVG(tp_min) AS "tp_min", 
            AVG(tp_mean) AS "tp_mean",
            AVG(tp_max) AS "tp_max",
            AVG(e_min) AS "e_min", 
            AVG(e_mean) AS "e_mean",
            AVG(e_max) AS "e_max"
            FROM era5 
            WHERE EXTRACT(MONTH FROM time) = :month
            AND ST_DWithin(geometry, :closest_geo, 0)
            GROUP BY EXTRACT(DAY FROM time), EXTRACT(MONTH FROM time),  geometry;
            """
            # AND ST_DWithin(geometry, 'SRID=3857;:z', 0);
            # kolom naam kan niet echt een variabel zijn. query builder api gebruiken.
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, month=month, closest_geo=closest_point).fetchall()
        return parse_daily_norm(res)

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
res = db.retrieve_norm(
    var="t2m_min", month=5, location=WGS84Point(latitude=-22.804, longitude=-54.383)
)
print(res)
print(len(res))
# print(res)
# print(res[0].keys())
