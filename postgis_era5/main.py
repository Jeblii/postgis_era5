from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
import pandas as pd
import geopandas as gpd
import psycopg2

# Creating SQLAlchemy's engine to use
# engine = create_engine('postgresql://localhost/jeffreytsang')



# geodataframe = gpd.GeoDataFrame(pd.DataFrame.from_csv('<your dataframe source>'))
# #... [do something with the geodataframe]

# geodataframe['geom'] = geodataframe['geometry'].apply(lambda x: WKTElement(x.wkt, srid=<your_SRID>)

# #drop the geometry column as it is now duplicative
# geodataframe.drop('geometry', 1, inplace=True)

# # Use 'dtype' to specify column's type
# # For the geom column, we will use GeoAlchemy's type 'Geometry'
# geodataframe.to_sql(table_name, engine, if_exists='append', index=False, 
#                          dtype={'geom': Geometry('POINT', srid= <your_srid>)})