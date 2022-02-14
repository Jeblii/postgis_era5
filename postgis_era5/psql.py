import sqlalchemy
from sqlalchemy.sql import text
from typing import List

from postgis_era5.parsing import parse_daily_weather, parse_daily_weather_norm, DailyWeather, DailyWeatherNorm
from postgis_era5.types import WGS84Point

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
            SELECT ST_AsText(geometry) FROM era5
            WHERE EXTRACT(MONTH FROM time) = 5 
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
            FROM era5 
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


