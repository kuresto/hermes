from enum import Enum
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import ChoiceType, UUIDType
from sqlalchemy_utils.models import Timestamp

from .db import BaseModel


class Status(Enum):
    start = "start"
    in_flight = "in_flight"
    processing = "processing"
    success = "success"
    error = "error"
    dead = "dead"


class MessageQueue(BaseModel, Timestamp):
    uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid4)

    scheduled_to = Column(DateTime, nullable=False)
    sender = Column(String(100), nullable=False)
    recipient = Column(String(100), nullable=False)

    content = Column(Text, nullable=True)

    status = Column(ChoiceType(Status, impl=String(20)), nullable=False)
    status_message = Column(String(200), nullable=True)

    history = relationship("MessageQueueHistory", backref="message")


class MessageQueueHistory(BaseModel, Timestamp):
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_uuid = Column(
        UUIDType(binary=False), ForeignKey(f"{MessageQueue.__tablename__}.uuid")
    )

    scheduled_to = Column(DateTime, nullable=False)
    sender = Column(String(100), nullable=False)
    recipient = Column(String(100), nullable=False)

    content = Column(Text, nullable=True)

    status = Column(ChoiceType(Status, impl=String(20)), nullable=False)
    status_message = Column(String(200), nullable=True)
