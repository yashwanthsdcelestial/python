from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import psycopg2
import psycopg2.errors

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def verify_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connection successful:", result.scalar())

def run_raw_query():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to Supabase successfully!")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users LIMIT 5;")
        rows = cur.fetchall()
        print("Users (raw SQL):")
        for row in rows:
            print(row)
        print(f"Rows fetched: {len(rows)}")
    except psycopg2.errors.UndefinedTable:
        print("Error: The 'users' table does not exist.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Connection closed.")
            
if __name__ == "__main__":
    run_raw_query()