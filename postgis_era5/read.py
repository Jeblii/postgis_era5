import statistics
from typing import List

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text

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
        return res[0]["st_astext"]

    def retrieve_norm(
        self, var: str, month: int, location: WGS84Point, year_range: int = 10
    ):

        closest_point = self.get_closest_point(location=location)
        closest_point = f"SRID=4326;{closest_point}"
        query = text(
            """
            SELECT * FROM era5 
            WHERE EXTRACT(MONTH FROM time) = :month
            AND ST_DWithin(geometry, :closest_geo, 0);
            """
            # AND ST_DWithin(geometry, 'SRID=3857;:z', 0);
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
res = db.retrieve_norm(
    var="t2m_min", month=5, location=WGS84Point(latitude=-22.804, longitude=-54.383)
)
print(res)
print(res[0].keys())
