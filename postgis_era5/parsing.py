import dataclasses as dc
import datetime
from postgis_era5.types import WGS84Point

@dc.dataclass
class DailyNorm:
    date: datetime.date
    location: WGS84Point
    temperature_min: float
    temperature_mean: float
    temperature_max: float
    dewpoint_temperature_min: float
    dewpoint_temperature_mean: float
    dewpoint_temperature_max: float
    east_wind_min: float
    east_wind_mean: float
    east_wind_max: float
    north_wind_min: float
    north_wind_mean: float
    north_wind_max: float
    leaf_area_index_high_vegetation_min: float
    leaf_area_index_high_vegetation_mean: float
    leaf_area_index_high_vegetation_max: float
    potential_evaporation_min: float
    potential_evaporation_mean: float
    potential_evaporation_max: float
    surface_latent_heat_flux_min: float
    surface_latent_heat_flux_mean: float
    surface_latent_heat_flux_max: float
    surface_net_solar_radiation_min: float
    surface_net_solar_radiation_mean: float
    surface_net_solar_radiation_max: float
    surface_net_thermal_radiation_min: float
    surface_net_thermal_radiation_mean: float
    surface_net_thermal_radiation_max: float
    surface_sensible_heat_flux_min: float
    surface_sensible_heat_flux_mean: float
    surface_sensible_heat_flux_max: float
    total_precipitation_min: float
    total_precipitation_mean: float
    total_precipitation_max: float
    total_evaporation_min: float
    total_evaporation_mean: float
    total_evaporation_max: float

