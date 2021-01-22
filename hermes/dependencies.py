from typing import AsyncIterable

from fastapi import Depends
from sqlalchemy.engine import Engine as Database
from sqlalchemy.orm import Session

from .db import db_conn


async def get_db_conn() -> Database:
    assert db_conn is not None
    return db_conn


async def get_db_session(conn=Depends(get_db_conn)) -> AsyncIterable[Session]:
    session = Session(bind=conn)

    try:
        yield session
    finally:
        session.close()
