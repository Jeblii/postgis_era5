from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import pandas as pd
import geopandas as gpd
import psycopg2
import xarray as xr
import netCDF4 as nc
from shapely.geometry import Point


def main():
    def apply_transformation(era5_df: pd.DataFrame()) -> pd.DataFrame():
        era5_df["d2m"] = era5_df.d2m - 273.15  # K to celcius
        era5_df["t2m"] = era5_df.t2m - 273.15  # K to celcius
        era5_df["pev"] = era5_df["pev"] * 1000
        era5_df["tp"] = era5_df["tp"] * 1000
        return era5_df

    # Creating SQLAlchemy's engine to use
    engine = create_engine("postgresql://localhost/era5")

    ds = xr.open_dataset(
        "/Users/jeffreytsang/OneDrive - Raboweb/Documents/Notebooks/weather_data_vendor_trials/era5/sicredi/era5_2011.nc"
    )
    df = ds.to_dataframe()
    df.dropna(inplace=True)

    # df = apply_transformation(df)
    reset_index_df = df.reset_index()
    geom = [
        Point(x, y)
        for x, y in zip(reset_index_df["longitude"], reset_index_df["latitude"])
    ]
    gdf = gpd.GeoDataFrame(reset_index_df, geometry=geom)
    gdf.drop(columns=["latitude", "longitude"], inplace=True)
    gdf = gdf.set_crs("epsg:4326")
    print(gdf.head(), gdf.crs, gdf.dtypes)

    gdf.to_postgis(name="era5", con=engine, if_exists='append')


if __name__ == "__main__":
    main()
