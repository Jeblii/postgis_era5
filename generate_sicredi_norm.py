import pandas as pd
from ast import literal_eval
from postgis_era5.types import WGS84Point
from postgis_era5.psql import PSQLInterface
from sqlalchemy import create_engine
from pprint import pprint
import time

MONTHS = range(1, 13)

"""
connect to DB
"""
db_string = "postgresql://localhost/era5"  # link to local postgres table
db_connection = create_engine(db_string)

db = PSQLInterface(db_connection)
db.check_connection()

"""
load in previous sicredi data set for finding points to ingest
"""
fn = "/Users/jeffreytsang/OneDrive - Raboweb/Documents/Notebooks/Sicredi/historical_weather_new_plots.csv"

df = pd.read_csv(fn)
df = df[
    df.municipality != "municipality"
]  # filter out rows with header as vlaues(error in appendign)

coords = [
    WGS84Point(literal_eval(coord)[0], literal_eval(coord)[1])
    for coord in df.center_coord.unique()
]
print(len(coords))

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
