from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults

from .base import BaseModelMixin
from .settings import DATABASE_URI

engine = create_engine(DATABASE_URI)
session_factory = sessionmaker(engine)
session = scoped_session(session_factory)

BaseModel = declarative_base(engine, cls=BaseModelMixin)
BaseModel.query = session.query_property()
force_auto_coercion()
force_instant_defaults()
