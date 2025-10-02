from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# ------------------------------
# Database URL
# ------------------------------
# Use DATABASE_URL from .env (PostgreSQL in production)
# Fallback to SQLite locally
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./lang_analyzer.db")

# ------------------------------
# SQLAlchemy Engine
# ------------------------------
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {}
)

# ------------------------------
# Session maker
# ------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ------------------------------
# Base class for models
# ------------------------------
Base = declarative_base()

# ------------------------------
# Dependency for FastAPI endpoints
# ------------------------------
def get_db() -> Session:
    """
    Provides a SQLAlchemy database session for FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
