from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import ChoiceType, UUIDType
from sqlalchemy_utils.models import Timestamp

from .db import BaseModel as DeclarativeBaseModel
from .db import session
from .enums import MessageStatus


class BaseModel(DeclarativeBaseModel):
    __abstract__ = True

    query = session.query_property()


class CrudModel(BaseModel):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def exists(cls, *args):
        exists = cls.query.exists()

        for arg in args:
            exists = exists.where(arg)

        return session.query(exists).scalar()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save(commit)

    def save(self, commit=True):
        session.add(self)
        if commit:
            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                raise exc
        return self

    def delete(self, commit=True):
        session.delete(self)
        return commit and session.commit()


class MessageQueue(Timestamp, CrudModel):
    uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid4)

    scheduled_to = Column(DateTime, nullable=False)
    sender = Column(String(100), nullable=False)
    recipient = Column(String(100), nullable=False)

    content = Column(Text, nullable=True)

    status = Column(
        ChoiceType(MessageStatus, impl=String(20)),
        default=MessageStatus.start,
        nullable=False,
    )
    status_message = Column(String(200), nullable=True)

    history = relationship("MessageQueueHistory", backref="message")


class MessageQueueHistory(Timestamp, CrudModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_uuid = Column(
        UUIDType(binary=False), ForeignKey(f"{MessageQueue.__tablename__}.uuid")
    )

    scheduled_to = Column(DateTime, nullable=False)
    sender = Column(String(100), nullable=False)
    recipient = Column(String(100), nullable=False)

    content = Column(Text, nullable=True)

    status = Column(
        ChoiceType(MessageStatus, impl=String(20)),
        default=MessageStatus.start,
        nullable=False,
    )
    status_message = Column(String(200), nullable=True)
