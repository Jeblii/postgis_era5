import time
from postgis_era5.types import WGS84Point
from postgis_era5.psql import PSQLInterface
from sqlalchemy import create_engine
from pprint import pprint

db_string = "postgresql://localhost/era5" #link to local postgres table
db_connection = create_engine(db_string)

db = PSQLInterface(db_connection)
db.check_connection()

tic = time.perf_counter()
res = db.retrieve_monthly_norm(
    month=5, location=WGS84Point(latitude=-22.804, longitude=-54.383)
)
pprint(res)
print(len(res))
# res = db.retrieve_monthly_historical_observations(
#     month=5, year=2020, location=WGS84Point(latitude=-22.804, longitude=-54.383)
# )
# # pprint(res)
# print(len(res))
toc = time.perf_counter()
print(f"{toc - tic:0.4f} seconds")