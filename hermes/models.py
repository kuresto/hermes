from sqlalchemy.ext.declarative.api import declared_attr


class BaseModelMixin:
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    __mapper_args__ = {"always_refresh": True}
