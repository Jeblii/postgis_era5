import psycopg2

conn = psycopg2.connect(host="localhost", port="5432")
conn.autocommit = True

cursor = conn.cursor()
post_gis_database_name = "era5"
name_Database = str(post_gis_database_name)

sql = "create database " + str(name_Database)

cursor.execute(sql)
print("Database created successfully, add post-GIS extension to it........")

conn.close()
