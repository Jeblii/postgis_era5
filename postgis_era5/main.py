import os

import geopandas as gpd
import netCDF4 as nc
import pandas as pd
import psycopg2
import xarray as xr
from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import Point
from sqlalchemy import *


def main():
    def apply_transformation(era5_df: pd.DataFrame()) -> pd.DataFrame():
        era5_df.loc[:, era5_df.columns.str.contains("d2m")] -= 273.15
        era5_df.loc[:, era5_df.columns.str.contains("t2m")] -= 273.15
        era5_df.loc[:, era5_df.columns.str.contains("pev")] *= 1000
        era5_df.loc[:, era5_df.columns.str.contains("tp")] *= 1000
        return era5_df

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

        # resample to daily values
        agg_df = df.groupby(
            [
                pd.Grouper(level="latitude"),
                pd.Grouper(level="longitude"),
                pd.Grouper(level="time", freq="D"),
            ]
        ).agg(["min", "max", "mean"])
        agg_df.columns = ["_".join(col) for col in agg_df.columns]

        agg_df = apply_transformation(agg_df)
        reset_index_df = agg_df.reset_index()
        geom = [
            Point(x, y)
            for x, y in zip(reset_index_df["longitude"], reset_index_df["latitude"])
        ]
        gdf = gpd.GeoDataFrame(reset_index_df, geometry=geom)
        gdf.drop(columns=["latitude", "longitude"], inplace=True)
        gdf = gdf.set_crs("epsg:4326")
        print(gdf.head(), gdf.crs, gdf.dtypes)

        gdf.to_postgis(name="era5", con=engine, if_exists="append")


if __name__ == "__main__":
    main()
