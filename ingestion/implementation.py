import requests
import cdsapi
from typing import List
from ingestion.constants import VARIABLES, DAYS, MONTHS, TIME

class CdsAPI:
    session: requests.Session
    cds_api: cdsapi.Client

    def __init__(self, session: requests.Session, cds_api: cdsapi.Client) -> None:
        self.session = session
        self.cds_api = cds_api

    def get_era5_land(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        year: int,
        region: str,
    ) -> None:
        self.cds.retrieve(
            "reanalysis-era5-land",
            {
                "variable": VARIABLES,
                "year": year,
                "month": MONTHS,
                "day": DAYS,
                "time": TIME,
                "area": [
                    min_lat,
                    min_lon,
                    max_lat,
                    max_lon,  # min lat, #min lon, #max lat, #max lon
                ],
                "format": "netcdf",
            },
            f"/Users/jeffreytsang/OneDrive - Raboweb/Documents/Notebooks/weather_data_vendor_trials/era5/BP/era5_{region}_{year}.nc",
        )

        return None
