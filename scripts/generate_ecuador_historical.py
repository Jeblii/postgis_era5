# 2015 <> 2018
import pandas as pd
from ast import literal_eval
from src.postgis_era5.types import WGS84Point
from src.postgis_era5.psql import PSQLInterface
from sqlalchemy import create_engine
from pprint import pprint
import time

MONTHS = range(1, 13)
YEARS = [2015, 2016, 2017, 2018]

"""
connect to DB
"""
db_string = "postgresql://localhost/era5"  # link to local postgres table
db_connection = create_engine(db_string)

db = PSQLInterface(db_connection)
db.check_connection()


"""
query to retrieve the same data
"""
tic = time.perf_counter()
hist_df = pd.DataFrame()
for year in YEARS:
    for month in MONTHS:
        res = db.retrieve_monthly_historical_observations(
            month=month, year=year
        )
        res_df = pd.DataFrame.from_records([day.__dict__ for day in res])

        hist_df = hist_df.append(res_df)

print(hist_df.head())
print(hist_df.shape)
toc = time.perf_counter()
print(f"{toc - tic:0.4f} seconds")

hist_df.to_csv("output_files/historical_ecuador_weather2.csv", index=False)
