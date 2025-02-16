from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from config.settings import get_settings

env = get_settings()

engine = create_engine(
    env.POSTGRES_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()


SessionDep = Annotated[Session, Depends(get_db)]
