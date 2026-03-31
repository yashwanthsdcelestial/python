from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import re

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def mask_database_url(url):
    return re.sub(r'://([^:]+):([^@]+)@', r'://\1:***@', url)

engine = create_engine(DATABASE_URL, echo=False)
print(f"Engine created: {mask_database_url(DATABASE_URL)}")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
print("Session factory ready.")

Base = declarative_base()

def verify_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Connection verified: SELECT 1 returned 1")
            print("Database connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify_connection()