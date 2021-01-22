# pylint: disable=unsubscriptable-object, global-statement
from typing import Optional

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine as Database
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults

from .base import BaseModelMixin
from .settings import DATABASE_URL

# Prepare the engine and session for usage
engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(engine)

# Instance and configure session
session = scoped_session(session_factory)
db_conn: Optional[Database] = engine

BaseModel = declarative_base(engine, cls=BaseModelMixin)
BaseModel.query = session.query_property()
force_auto_coercion()
force_instant_defaults()
