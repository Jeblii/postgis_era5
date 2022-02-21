import dataclasses as dc
import datetime
from typing import List, Mapping

from src.postgis_era5.types import WGS84Point


"""
temp: min, max, mean
precipitation: sum
humidity: max, min
daily_max_wind
daily_mean wind
gdd
"""

@dc.dataclass
class DailyWeatherNorm:
    month: int
    day: int
    location: WGS84Point
    temperature_min_avg: float
    temperature_min_stdev: float
    temperature_mean_avg: float
    temperature_mean_stdev: float
    temperature_max_avg: float
    temperature_max_stdev: float
    soil_temperature_1m_min_avg: float
    soil_temperature_1m_min_stdev: float
    soil_temperature_1m_mean_avg: float
    soil_temperature_1m_mean_stdev: float
    soil_temperature_1m_max_avg: float
    soil_temperature_1m_max_stdev: float
    dewpoint_temperature_min_avg: float
    dewpoint_temperature_min_stdev: float
    dewpoint_temperature_mean_avg: float
    dewpoint_temperature_mean_stdev: float
    dewpoint_temperature_max_avg: float
    dewpoint_temperature_max_stdev: float
    wind_mean_avg: float
    wind_mean_stdev: float
    wind_max_avg: float
    wind_max_stdev: float
    pet_mean_avg: float
    pet_mean_stdev: float
    gdd_avg: float
    gdd_stdev: float
    net_radiation_avg: float
    net_radiation_stdev: float
    surface_net_solar_radiation_avg: float
    surface_net_solar_radiation_stdev: float
    surface_net_thermal_radiation_avg: float
    surface_net_thermal_radiation_stdev: float
    total_precipitation_sum_avg: float
    total_precipitation_sum_stdev: float


@dc.dataclass
class DailyWeather:
    date: datetime.date
    location: WGS84Point
    temperature_min: float
    temperature_mean: float
    temperature_max: float
    soil_temperature_1m_min: float
    soil_temperature_1m_mean: float
    soil_temperature_1m_max: float
    dewpoint_temperature_min: float
    dewpoint_temperature_mean: float
    dewpoint_temperature_max: float
    wind_min: float
    wind_mean: float
    wind_max: float
    pet_mean: float
    gdd: float
    net_radiation: float
    surface_net_solar_radiation: float
    surface_net_thermal_radiation: float
    total_precipitation_sum: float


def parse_daily_weather_norm(rows: Mapping[str, object]) -> List[DailyWeatherNorm]:
    daily_norms = [
        DailyWeatherNorm(
            month=row["month"],
            day=row["day"],
            location=row["geometry"],
            temperature_min_avg=row['t2m_min_avg'],
            temperature_min_stdev=row['t2m_min_stdev'],
            temperature_mean_avg=row['t2m_mean_avg'],
            temperature_mean_stdev=row['t2m_mean_stdev'],
            temperature_max_avg=row['t2m_max_avg'],
            temperature_max_stdev=row['t2m_max_stdev'],
            soil_temperature_1m_min_avg=row['stl1_min_avg'],
            soil_temperature_1m_min_stdev=row['stl1_min_stdev'],
            soil_temperature_1m_mean_avg=row['stl1_mean_avg'],
            soil_temperature_1m_mean_stdev=row['stl1_mean_stdev'],
            soil_temperature_1m_max_avg=row['stl1_max_avg'],
            soil_temperature_1m_max_stdev=row['stl1_max_stdev'],
            dewpoint_temperature_min_avg=row['d2m_min_avg'],
            dewpoint_temperature_min_stdev=row['d2m_min_stdev'],
            dewpoint_temperature_mean_avg=row['d2m_mean_avg'],
            dewpoint_temperature_mean_stdev=row['d2m_mean_stdev'],
            dewpoint_temperature_max_avg=row['d2m_max_avg'],
            dewpoint_temperature_max_stdev=row['d2m_max_stdev'],
            wind_mean_avg=row['ws_2m_mean_avg'],
            wind_mean_stdev=row['ws_2m_mean_stdev'],
            wind_max_avg=row['ws_2m_max_avg'],
            wind_max_stdev=row['ws_2m_max_stdev'],
            pet_mean_avg=row['daily_pet_mean_avg'],
            pet_mean_stdev=row['daily_pet_mean_stdev'],
            gdd_avg=row['gdd_avg'],
            gdd_stdev=row['gdd_stdev'],
            net_radiation_avg=row['nr_avg'],
            net_radiation_stdev=row['nr_stdev'],
            surface_net_solar_radiation_avg=row['ssr_avg'],
            surface_net_solar_radiation_stdev=row['ssr_stdev'],
            surface_net_thermal_radiation_avg=row['str_avg'],
            surface_net_thermal_radiation_stdev=row['str_stdev'],
            total_precipitation_sum_avg=row['tp_avg'],
            total_precipitation_sum_stdev=row['tp_stdev'],
        )
        for row in rows
    ]
    return daily_norms


def parse_daily_weather(rows: Mapping[str, object]) -> List[DailyWeather]:
    daily_weather = [
        DailyWeather(
            date=row["time"].date(),
            location=row["geometry"],
            temperature_min=row["t2m_min"],
            temperature_mean=row["t2m_mean"],
            temperature_max=row["t2m_max"],
            soil_temperature_1m_min=row['stl1_min'],
            soil_temperature_1m_mean=row['stl1_mean'],
            soil_temperature_1m_max=row['stl1_max'],
            dewpoint_temperature_min=row["d2m_min"],
            dewpoint_temperature_mean=row["d2m_mean"],
            dewpoint_temperature_max=row["d2m_max"],
            wind_mean=row["ws_2m_mean"],
            wind_max=row["ws_2m_max"],
            pet_mean=row['daily_pet_mean'],
            gdd=row['gdd'],
            net_radiation=row['nr'],
            surface_net_solar_radiation=row['ssr_max'],
            surface_net_thermal_radiation=row['str_min'],
            total_precipitation_sum=row['tp_sum'],
        )
        for row in rows
    ]
    return daily_weather
