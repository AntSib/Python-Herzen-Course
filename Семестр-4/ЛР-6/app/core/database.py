from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager
from typing import Generator
import os


FILE_PATH:  str = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH:  str = os.path.dirname(FILE_PATH)
DB_DIR:     str = os.path.join(ROOT_PATH, 'db')
DB_PATH:    str = os.path.join(DB_DIR, 'logtable.db')

if not os.path.exists(DB_DIR):
    os.mkdir(DB_DIR)


SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session.

    :param Session: the session class to use, defaults to SessionLocal
    :return: a session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
