import psycopg2
import sys

PASSWORD = "22122003Yashwanth$D"

try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password=PASSWORD, host="localhost", port=5432)
    print("Connected successfully")
except psycopg2.OperationalError as e:
    print(f"Connection failed: {e}")
    print("Edit setup_db.py and fix the PASSWORD variable")
    sys.exit(1)

conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'exam_db'")
cur.execute("DROP DATABASE IF EXISTS exam_db")
cur.execute("CREATE DATABASE exam_db")
conn.close()
print("Database recreated successfully")
