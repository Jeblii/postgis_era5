import time
from ast import literal_eval
from pprint import pprint

import pandas as pd
from sqlalchemy import create_engine

from config import config
from src.postgis_era5.psql import PSQLInterface
from src.postgis_era5.types import WGS84Point
from shapely import wkt
import geopandas as gpd
import shapely
"""
get farm data
"""
fn = "/Users/jeffreytsang/OneDrive - Raboweb/Documents/DELETE_ASAP/BP_geolocations_anonomysed.csv"

df = pd.read_csv(fn)
df.dropna(inplace=True)

df['geometry'] = df['geometry'].apply(lambda x: wkt.loads(x))
gdf = gpd.GeoDataFrame(df, geometry=df.geometry)
"""
creating bounding box using min lat, min lon, max lat, max lon
"""
xmin, ymin, xmax, ymax = gdf.total_bounds

"""
load in data set needed
"""
weather_df = pd.read_csv('/Users/jeffreytsang/Desktop/rabobank/bp/norm_bp_weather.csv')

weather_df['location'] = weather_df['location'].apply(lambda x: shapely.wkt.loads(x))
weather_gdf = gpd.GeoDataFrame(weather_df, geometry='location')

filtered_norm_gdf = weather_gdf.cx[xmin:xmax, ymin:ymax]

filtered_norm_gdf.to_csv("output_files/norm_bp_weather_filtered.csv", index=False)


