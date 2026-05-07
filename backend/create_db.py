import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="hi"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE timetable_db;")
    cur.close()
    conn.close()
    print("Database timetable_db created successfully.")
except Exception as e:
    print(f"Error: {e}")
