import psycopg2

def main():
    conn1 = psycopg2.connect(dbname='era5', host='localhost', port= '5432')
    conn1.autocommit = True
    cursor = conn1.cursor()
    cursor.execute("CREATE EXTENSION postgis;")
    conn1.commit()
    cursor.close()
    conn1.close()

if __name__ == "__main__":
    main()