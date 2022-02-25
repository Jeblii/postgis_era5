import time
from ast import literal_eval
from pprint import pprint

import pandas as pd
from config import config
from sqlalchemy import create_engine
from src.postgis_era5.psql import PSQLInterface
from src.postgis_era5.types import WGS84Point

MONTHS = range(1, 13)

"""
connect to DB
"""
db_string = config.database_url  # link to local postgres table
db_connection = create_engine(db_string)

db = PSQLInterface(db_connection)
db.check_connection()

"""
query to retrieve the same data
"""
tic = time.perf_counter()
norm_df = pd.DataFrame()
for month in MONTHS:
    res = db.retrieve_monthly_norm(month=month)
    res_df = pd.DataFrame.from_records([day.__dict__ for day in res])

    norm_df = norm_df.append(res_df)

print(norm_df.head())
print(norm_df.shape)
toc = time.perf_counter()
print(f"{toc - tic:0.4f} seconds")

norm_df.to_csv("output_files/norm_bp_weather2.csv", index=False)
