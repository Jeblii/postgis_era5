from urllib import request

import cdsapi
from ingestion.implementation import CdsAPI

cds = cdsapi.Client()

api = CdsAPI(cds_api=cds)
years = range(2012, 2019)
for year in years:
    api.get_era5_land(
        min_lat=-4.959615,
        max_lat=1.450040,
        min_lon=-81.430664,
        max_lon=-75.585938,
        year=year,
        region="parana_brazil",
    )
