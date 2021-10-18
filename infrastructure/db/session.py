from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    global db
    try:
        db = localSession()
        yield db
    finally:
        db.close()
