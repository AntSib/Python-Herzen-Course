import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./glossary.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine),
)
Base = declarative_base()
