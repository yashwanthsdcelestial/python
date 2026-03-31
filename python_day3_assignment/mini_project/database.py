"""Database configuration and session management."""
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    poolclass=pool.QueuePool,
    pool_size=5,
    pool_pre_ping=True,   # Test connections before using
    pool_recycle=3600,    # Recycle connections every hour
    echo=settings.debug   # Log SQL statements if debug mode
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency injection for database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db(reset: bool = False):
    """
    Initialize database.
    
    Args:
        reset (bool): If True, drops all tables before creating them.
                      Use ONLY for development/testing.
    """
    try:
        if reset:
            logger.warning("⚠️ Dropping all tables...")
            Base.metadata.drop_all(bind=engine)

        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)

        logger.info("✅ Database tables initialized")

    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def close_db():
    """Close database connection pool."""
    try:
        engine.dispose()
        logger.info("✅ Database connection pool closed")
    except Exception as e:
        logger.error(f"Error closing database: {str(e)}")