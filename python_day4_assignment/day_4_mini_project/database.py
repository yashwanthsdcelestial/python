from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings
from decorators.retry import retry
import logging

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


@retry(max_attempts=3)
def verify_connection(engine):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("Database connection verified.")


engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()