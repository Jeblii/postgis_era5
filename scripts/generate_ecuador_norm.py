import pandas as pd
from ast import literal_eval
from postgis_era5.types import WGS84Point
from postgis_era5.psql import PSQLInterface
from sqlalchemy import create_engine
from pprint import pprint
import time
from config import config

MONTHS = range(1, 13)

"""
connect to DB
"""
db_string = config.database_url  # link to local postgres table
db_connection = create_engine(db_string)

db = PSQLInterface(db_connection)
db.check_connection()

"""
get all unique points
"""

"""
query to retrieve the same data
"""
tic = time.perf_counter()
norm_df = pd.DataFrame()
for coord in coords:
    for month in MONTHS:
        res = db.retrieve_monthly_norm(month=month, location=coord)
        res_df = pd.DataFrame.from_records([day.__dict__ for day in res])
        res_df["latitude"] = coord.latitude
        res_df["longitude"] = coord.longitude

        norm_df = norm_df.append(res_df)

print(norm_df.head())
print(norm_df.shape)
toc = time.perf_counter()
print(f"{toc - tic:0.4f} seconds")

norm_df.to_csv("output_files/norm_sicredi_weather.csv", index=False)
