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
    pet_max_avg: float
    pet_max_stdev: float
    gdd_avg: float
    gdd_stdev: float
    net_radiation_min_avg: float
    net_radiation_min_stdev: float
    net_radiation_mean_avg: float
    net_radiation_mean_stdev: float
    net_radiation_max_avg: float
    net_radiation_max_stdev: float
    surface_net_solar_radiation_min_avg: float
    surface_net_solar_radiation_min_stdev: float
    surface_net_solar_radiation_mean_avg: float
    surface_net_solar_radiation_mean_stdev: float
    surface_net_solar_radiation_max_avg: float
    surface_net_solar_radiation_max_stdev: float
    surface_net_thermal_radiation_min_avg: float
    surface_net_thermal_radiation_min_stdev: float
    surface_net_thermal_radiation_mean_avg: float
    surface_net_thermal_radiation_mean_stdev: float
    surface_net_thermal_radiation_max_avg: float
    surface_net_thermal_radiation_max_stdev: float
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
    pet_max: float
    gdd: float
    net_radiation_min: float
    net_radiation_mean: float
    net_radiation_max: float
    surface_net_solar_radiation_min: float
    surface_net_solar_radiation_mean: float
    surface_net_solar_radiation_max: float
    surface_net_thermal_radiation_min: float
    surface_net_thermal_radiation_mean: float
    surface_net_thermal_radiation_max: float
    total_precipitation_sum: float


def parse_daily_weather_norm(rows: Mapping[str, object]) -> List[DailyWeatherNorm]:
    daily_norms = [
        DailyWeatherNorm(
            month=row["month"],
            day=row["day"],
            location=row["geometry"],
            temperature_min_avg=row["t2m_min_avg"],
            temperature_min_stdev=row["t2m_min_stdev"],
            temperature_mean_avg=row["t2m_mean_avg"],
            temperature_mean_stdev=row["t2m_mean_stdev"],
            temperature_max_avg=row["t2m_max_avg"],
            temperature_max_stdev=row["t2m_max_stdev"],
            dewpoint_temperature_min=row["d2m_min"],
            dewpoint_temperature_mean=row["d2m_mean"],
            dewpoint_temperature_max=row["d2m_max"],
            east_wind_min=row["u10_min"],
            east_wind_mean=row["u10_mean"],
            east_wind_max=row["u10_max"],
            north_wind_min=row["v10_min"],
            north_wind_mean=row["v10_mean"],
            north_wind_max=row["v10_max"],
            leaf_area_index_high_vegetation_min=row["lai_hv_min"],
            leaf_area_index_high_vegetation_mean=row["lai_hv_mean"],
            leaf_area_index_high_vegetation_max=row["lai_hv_max"],
            potential_evaporation_min=row["pev_min"],
            potential_evaporation_mean=row["pev_mean"],
            potential_evaporation_max=row["pev_max"],
            surface_latent_heat_flux_min=row["slhf_min"],
            surface_latent_heat_flux_mean=row["slhf_mean"],
            surface_latent_heat_flux_max=row["slhf_max"],
            surface_net_solar_radiation_min=row["ssr_min"],
            surface_net_solar_radiation_mean=row["ssr_mean"],
            surface_net_solar_radiation_max=row["ssr_max"],
            surface_net_thermal_radiation_min=row["str_min"],
            surface_net_thermal_radiation_mean=row["str_mean"],
            surface_net_thermal_radiation_max=row["str_max"],
            surface_sensible_heat_flux_min=row["sshf_min"],
            surface_sensible_heat_flux_mean=row["sshf_mean"],
            surface_sensible_heat_flux_max=row["sshf_max"],
            total_precipitation_min=row["tp_min"],
            total_precipitation_mean=row["tp_mean"],
            total_precipitation_max=row["tp_max"],
            total_evaporation_min=row["e_min"],
            total_evaporation_mean=row["e_mean"],
            total_evaporation_max=row["e_max"],
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
            dewpoint_temperature_min=row["d2m_min"],
            dewpoint_temperature_mean=row["d2m_mean"],
            dewpoint_temperature_max=row["d2m_max"],
            east_wind_min=row["u10_min"],
            east_wind_mean=row["u10_mean"],
            east_wind_max=row["u10_max"],
            north_wind_min=row["v10_min"],
            north_wind_mean=row["v10_mean"],
            north_wind_max=row["v10_max"],
            leaf_area_index_high_vegetation_min=row["lai_hv_min"],
            leaf_area_index_high_vegetation_mean=row["lai_hv_mean"],
            leaf_area_index_high_vegetation_max=row["lai_hv_max"],
            potential_evaporation_min=row["pev_min"],
            potential_evaporation_mean=row["pev_mean"],
            potential_evaporation_max=row["pev_max"],
            surface_latent_heat_flux_min=row["slhf_min"],
            surface_latent_heat_flux_mean=row["slhf_mean"],
            surface_latent_heat_flux_max=row["slhf_max"],
            surface_net_solar_radiation_min=row["ssr_min"],
            surface_net_solar_radiation_mean=row["ssr_mean"],
            surface_net_solar_radiation_max=row["ssr_max"],
            surface_net_thermal_radiation_min=row["str_min"],
            surface_net_thermal_radiation_mean=row["str_mean"],
            surface_net_thermal_radiation_max=row["str_max"],
            surface_sensible_heat_flux_min=row["sshf_min"],
            surface_sensible_heat_flux_mean=row["sshf_mean"],
            surface_sensible_heat_flux_max=row["sshf_max"],
            total_precipitation_min=row["tp_min"],
            total_precipitation_mean=row["tp_mean"],
            total_precipitation_max=row["tp_max"],
            total_evaporation_min=row["e_min"],
            total_evaporation_mean=row["e_mean"],
            total_evaporation_max=row["e_max"],
        )
        for row in rows
    ]
    return daily_weather
