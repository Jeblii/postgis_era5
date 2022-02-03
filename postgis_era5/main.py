from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import pandas as pd
import geopandas as gpd
import psycopg2
import xarray as xr
import netCDF4 as nc
from shapely.geometry import Point

def apply_transformation(era5_df: pd.DataFrame()) -> pd.DataFrame():
    era5_df['d2m'] = era5_df.d2m - 273.15 # K to celcius
    era5_df['t2m'] = era5_df.t2m - 273.15 # K to celcius
    era5_df['pev'] = era5_df['pev'] * 1000
    era5_df['tp'] = era5_df['tp'] * 1000
    return era5_df

ds = xr.open_dataset('/Users/jeffreytsang/OneDrive - Raboweb/Documents/Notebooks/weather_data_vendor_trials/era5/sicredi/era5_2021.nc')
df = ds.to_dataframe()
df.dropna(inplace=True)

# Creating SQLAlchemy's engine to use
engine = create_engine('postgresql://localhost/era5')

df = apply_transformation(df)
reset_index_df = df.reset_index()
geom = [Point(x,y) for x, y in zip(reset_index_df['longitude'], reset_index_df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geom)
print(gdf.head())

gdf.to_postgis(name='era5', con=engine)
# geodataframe['geom'] = geodataframe['geometry'].apply(lambda x: WKTElement(x.wkt, srid=<your_SRID>)

# #drop the geometry column as it is now duplicative
# geodataframe.drop('geometry', 1, inplace=True)

# # Use 'dtype' to specify column's type
# # For the geom column, we will use GeoAlchemy's type 'Geometry'
# geodataframe.to_sql(table_name, engine, if_exists='append', index=False, 
#                          dtype={'geom': Geometry('POINT', srid= <your_srid>)})