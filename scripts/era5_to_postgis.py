"""
SCRIPT FOR WRITING THE ERA5 NC FILES DOWNLOADED WITH THE CDSAPI TO MY POSTGIS
"""

import os
from typing import List

import geopandas as gpd
import netCDF4 as nc
import pandas as pd
import psycopg2
import xarray as xr
from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import Point
from sqlalchemy import *
from src.ingestion.conversions import *

def retrive_nc_files(path: str) -> List[str]:
    pass

def main():

    # Creating SQLAlchemy's engine to use
    engine = create_engine("postgresql://localhost/era5")

    nc_files = []
    for _, _, files in os.walk(
        "/Users/jeffreytsang/OneDrive - Raboweb/Documents/Notebooks/weather_data_vendor_trials/era5/sicredi/"
    ):
        for name in files:
            if name.endswith((".nc")):
                nc_files.append(name)

    for file in nc_files:
        print(file)
        ds = xr.open_dataset(
            f"/Users/jeffreytsang/OneDrive - Raboweb/Documents/Notebooks/weather_data_vendor_trials/era5/sicredi/{file}"
        )
        df = ds.to_dataframe()
        df.dropna(inplace=True)

        # conversions and derived variables
        df.d2m = kelvin_to_celcius(df.d2m)
        df.t2m = kelvin_to_celcius(df.t2m)
        df.tp = meters_to_mm(df.tp)
        df["ws_10m"] = wind_speed_from_u_v(df.u10, df.v10)
        df["ws_2m"] = wind_speed_10m_2m(df.ws_10m)
        df["nr"] = net_radation(df.ssr, (df.str))

        # resample to daily values
        agg_df = df.groupby(
            [
                pd.Grouper(level="latitude"),
                pd.Grouper(level="longitude"),
                pd.Grouper(level="time", freq="D"),
            ]
        ).agg(
            {
                "d2m": ["min", "mean", "max"],
                "t2m": ["min", "mean", "max"],
                "stl1": ["min", "mean", "max"],
                "ssr": [
                    "max"
                ],  # the max gets the accumulated radiation over the whole day
                "str": [
                    "max"
                ],  # the max gets the accumulated radiation over the whole day
                "sp": [
                    "mean"
                ],  # this is a feature that don't really deviate and is only used to calculate pet
                "tp": ["sum"],  # sum total precipitation on a day
                "ws_2m": ["mean", "max"],
                "nr": ["min", "mean", "max"],
                "rh": ["min", "mean", "max"],
                "G": ["min", "mean", "max"],
            }
        )
        agg_df.columns = ["_".join(col) for col in agg_df.columns]

        # GDD
        agg_df.gdd = daily_gdd(agg_df.t2m_max, agg_df.t2m_min)

        # PET mean
        agg_df["daily_pet_mean"] = calculate_pet(
            surface_pressure_KPa=agg_df.sp_mean / 1000,  # from pa to Kpa
            temperature2m_C=agg_df.t2m_mean,
            dewpoint2m_C=agg_df.d2m_mean,
            windspeed2m_m_s=agg_df.ws_2m_mean,
            net_radiation_MJ_m2=agg_df.nr_mean / 1000000,  # from joule -> megajoule
            soil_hf=agg_df.G_mean / 1000000,
            pet_time="daily",
        )

        # PET MAX
        agg_df["daily_pet_max"] = calculate_pet(
            surface_pressure_KPa=agg_df.sp_mean / 1000,  # from pa to Kpa
            temperature2m_C=agg_df.t2m_max,
            dewpoint2m_C=agg_df.d2m_max,
            windspeed2m_m_s=agg_df.ws_2m_max,
            net_radiation_MJ_m2=agg_df.nr_max / 1000000,  # from joule -> megajoule
            soil_hf=agg_df.G_max / 1000000,
            pet_time="daily",
        )

        # make geodataframe
        reset_index_df = agg_df.reset_index()
        gdf = gpd.GeoDataFrame(
            agg_df,
            geometry=gpd.points_from_xy(
                reset_index_df.longitude, reset_index_df.latitude
            ),
            crs="EPSG:4326",
        )
        gdf.drop(columns=["latitude", "longitude"], inplace=True)
        print(gdf.head(), gdf.crs, gdf.dtypes)

        gdf.to_postgis(name="era5_ecuador", con=engine, if_exists="append")


if __name__ == "__main__":
    main()
