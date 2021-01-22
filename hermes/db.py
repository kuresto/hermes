from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults

from hermes.settings import DATABASE_URI

engine = create_engine(DATABASE_URI)
session_factory = sessionmaker(engine)
session = scoped_session(session_factory)

# Todo: Move me to my file
class BaseModelMixin:
    @declared_attr
    def __tablename__(self):
        return f"hermes_{self.__name__.lower()}"

    __mapper_args__ = {"always_refresh": True}


BaseModel = declarative_base(engine, cls=BaseModelMixin)
force_auto_coercion()
force_instant_defaults()
