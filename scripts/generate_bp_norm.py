import time
from ast import literal_eval
from pprint import pprint

import pandas as pd
from sqlalchemy import create_engine

from config import config
from src.postgis_era5.psql import PSQLInterface
from src.postgis_era5.types import WGS84Point
from shapely import wkt

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

MONTHS = range(1, 13)

"""
connect to DB
"""
db_string = config.database_url  # link to local postgres table
db_connection = create_engine(db_string)

db = PSQLInterface(db_connection)
db.check_connection()

"""
get farm data
"""
fn = "/Users/jeffreytsang/OneDrive - Raboweb/Documents/DELETE_ASAP/BP_geolocations_anonomysed.csv"

df = pd.read_csv(fn)
df.dropna(inplace=True)

df['geometry'] = df['geometry'].apply(lambda x: wkt.loads(x))

"""
query to retrieve the same data
"""
tic = time.perf_counter()
norm_df = pd.DataFrame()
for idx, row in df.iterrows():
    print(idx, len(df))
    for month in MONTHS:
        res = db.retrieve_monthly_norm(month=month, location=WGS84Point(latitude=row.geometry.y, longitude=row.geometry.x))
        res_df = pd.DataFrame.from_records([day.__dict__ for day in res])
        res_df["farm_idgeom"] = row.geometry
        res_df['geo_id'] = row.geo_id

        norm_df = norm_df.append(res_df)

print(norm_df.head())
print(norm_df.shape)
toc = time.perf_counter()
print(f"{toc - tic:0.4f} seconds")

norm_df.to_csv("output_files/norm_bp_farm_weather.csv", index=False)
