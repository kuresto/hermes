from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .models import BaseModelMixin
from .settings import DATABASE_URI

engine = create_engine(DATABASE_URI)
session_factory = sessionmaker(engine)
session = scoped_session(session_factory)

BaseModel = declarative_base(engine, cls=BaseModelMixin)
