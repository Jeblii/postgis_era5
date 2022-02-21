import sqlalchemy
from sqlalchemy.sql import text
from typing import List

from src.postgis_era5.parsing import (
    parse_daily_weather,
    parse_daily_weather_norm,
    DailyWeather,
    DailyWeatherNorm,
)
from src.postgis_era5.types import WGS84Point
from psycopg2 import sql

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

    def get_closest_point(self, location: WGS84Point) -> str:
        # TODO(Jeffrey Tsang) this only works for point. Not yet tested for other types of geometry for behaviour. See also https://postgis.net/workshops/postgis-intro/knn.html
        wkt_text = f"SRID=4326;POINT({location.longitude} {location.latitude})"
        query = text(
            """
            SELECT ST_AsText(geometry) FROM era5_ecuador
            ORDER BY geometry::geometry <-> ST_GeomFromText(:wkt)::geometry
            LIMIT 1;
            """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, wkt=wkt_text).fetchall()
        return res[0]["st_astext"]

    def retrieve_monthly_norm(
        self, month: int, location: WGS84Point, year_range: int = 10
    ) -> List[DailyWeatherNorm]:

        closest_point = self.get_closest_point(location=location)
        closest_point = f"SRID=4326;{closest_point}"
        query = text(
            """
            SELECT 
            ST_AsText(geometry) AS "geometry",
            EXTRACT(DAY FROM time) AS "day",
            EXTRACT(MONTH FROM time) AS "month",
            AVG(t2m_min) AS "t2m_min_avg", 
            STDDEV(t2m_min) AS "t2m_min_stdev", 
            AVG(t2m_mean) AS "t2m_mean_avg",
            STDDEV(t2m_mean) AS "t2m_mean_stdev", 
            AVG(t2m_max) AS "t2m_max_avg",
            STDDEV(t2m_max) AS "t2m_max_stdev", 
            AVG(stl1_min) AS "stl1_min_avg", 
            STDDEV(stl1_min) AS "stl1_min_stdev", 
            AVG(stl1_mean) AS "stl1_mean_avg",
            STDDEV(stl1_mean) AS "stl1_mean_stdev", 
            AVG(stl1_max) AS "stl1_max_avg",
            STDDEV(stl1_max) AS "stl1_max_stdev",
            AVG(d2m_min) AS "d2m_min_avg", 
            STDDEV(d2m_min) AS "d2m_min_stdev", 
            AVG(d2m_mean) AS "d2m_mean_avg",
            STDDEV(d2m_mean) AS "d2m_mean_stdev", 
            AVG(d2m_max) AS "d2m_max_avg",
            STDDEV(d2m_max) AS "d2m_max_stdev",
            AVG(ws_2m_mean) AS "ws_2m_mean_avg",
            STDDEV(ws_2m_mean) AS "ws_2m_mean_stdev", 
            AVG(ws_2m_max) AS "ws_2m_max_avg",
            STDDEV(ws_2m_max) AS "ws_2m_max_stdev",
            AVG(daily_pet_mean) AS "daily_pet_mean_avg",
            STDDEV(daily_pet_mean) AS "daily_pet_mean_stdev",
            AVG(gdd) AS "gdd_avg",
            STDDEV(gdd) AS "gdd_stdev",
            AVG(nr) AS "nr_avg",
            STDDEV(nr) AS "nr_stdev",
            AVG(ssr_max) AS "ssr_avg",
            STDDEV(ssr_max) AS "ssr_stdev",
            AVG(str_min) AS "str_avg",
            STDDEV(str_min) AS "str_stdev",
            AVG(nr) AS "tp_avg",
            STDDEV(nr) AS "tp_stdev"
            FROM era5_ecuador 
            WHERE EXTRACT(MONTH FROM time) = :month
            AND ST_DWithin(geometry, :closest_geo, 0)
            GROUP BY EXTRACT(DAY FROM time), EXTRACT(MONTH FROM time),  geometry;
            """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, month=month, closest_geo=closest_point).fetchall()
        return parse_daily_weather_norm(res)

    def retrieve_monthly_historical_observations(
        self, month: int, year: int, location: WGS84Point
    ) -> List[DailyWeather]:
        closest_point = self.get_closest_point(location=location)
        closest_point = f"SRID=4326;{closest_point}"
        query = text(
            """
            SELECT *
            FROM era5_ecuador
            WHERE ST_DWithin(geometry, :closest_geo, 0)
            AND EXTRACT(MONTH FROM time) = :y 
            AND EXTRACT(YEAR FROM time) = :z;
            """
        )
        with self.engine.connect() as conn:
            res = conn.execute(
                query, y=month, z=year, closest_geo=closest_point
            ).fetchall()
        return parse_daily_weather(res)
