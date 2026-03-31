from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure SQLAlchemy connection pool for Supabase
engine = create_engine(
    DATABASE_URL,
    pool_size=5,             # max number of persistent connections
    max_overflow=10,         # additional temporary connections beyond pool_size
    pool_timeout=30,         # seconds to wait for connection before timeout
    pool_recycle=1800,       # recycle connections older than 1800 sec to avoid stale connections
    pool_pre_ping=True       # verify connection health for Supabase dropped idle connections
)

Session = sessionmaker(bind=engine)

sessions = []
for i in range(3):
    s = Session()
    s.execute(text("SELECT 1"))  # Force checkout and validate connection
    sessions.append(s)
    print(f"After opening session {i+1}: {engine.pool.status()}")

for s in sessions:
    s.close()

print(f"\nAfter closing all: {engine.pool.status()}")
