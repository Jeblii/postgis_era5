from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sqlalchemy
from typing import List
import statistics

db_string = "postgresql://localhost/era5"
db_connection = create_engine(db_string)

class PSQLInterface:

    engine: sqlalchemy.engine.base.Engine
    def __init__(self, engine:sqlalchemy.engine.base.Engine) -> None:
        self.engine = engine

    def check_connection(self) -> None:
        with self.engine.connect() as conn:
            res = conn.execute(
                """
                SELECT 1;
                """
            ).fetchall()
            if res != [(1,)]:
                raise Exception(
                    f"unexpected value when running the health check, expected [(1,)] but found {repr(res)}, "
                )

    def retrieve_norm(self, var:str, month: int, time_period: int=10):
        query = text(
            """
            SELECT AVG(:x) FROM era5 WHERE EXTRACT(MONTH FROM time) = :y;
            """
        )
        with self.engine.connect() as conn:
            res = conn.execute(query, x=var, y=month).fetchall()
        return res


db = PSQLInterface(db_connection)
db.check_connection()
res = db.retrieve_norm(var='t2m_min', month=5)
print(res)
# with db_connection.connect() as con:
#     # res = con.execute("SELECT * from spatial_ref_sys;")
#     # res = con.execute("SELECT * FROM era5 WHERE ST_Distance( geometry, 'SRID=4326;POINT(-4.960 -75.266)' ) < 0.01;")
#     # res = con.execute(
#     #     "SELECT ST_AsText(geometry) FROM era5 WHERE time >= '2011-05-10' AND time <  '2011-05-20' AND ST_Distance( geometry, 'SRID=4326;POINT(-54.383 -22.804)' ) < 0.01;"
#     # )
#     res = con.execute(
#         "SELECT AVG(t2m_min), AVG(t2m_mean), AVG(t2m_max) FROM era5 WHERE EXTRACT(MONTH FROM time) = 5;"
#     )
#     # res = con.execute(
#     #     "SELECT t2m_mean FROM era5 WHERE EXTRACT(MONTH FROM time) = 5;"
#     # )

# for r in res:
#     print(r)

# result = [r[0] for r in res]
# print(len(result))
# print(statistics.mean(result))
