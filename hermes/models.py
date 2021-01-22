from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import ChoiceType, UUIDType
from sqlalchemy_utils.models import Timestamp

from .db import BaseModel as DeclarativeBaseModel, session
from .logs import get_logger
from .enums import MessageStatus, MessageType


logger = get_logger(__name__)


class BaseModel(DeclarativeBaseModel):
    __abstract__ = True

    query = session.query_property()


class CrudModel(BaseModel):
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)

        logger.info(
            "Created new instance for %s with: %s",
            instance.__tablename__,
            instance.__dict__,
        )

        return instance.save()

    @classmethod
    def exists(cls, *args):
        exists = cls.query.exists()

        for arg in args:
            exists = exists.where(arg)

        return session.query(exists).scalar()

    def update(self, commit: bool = True, **kwargs):
        old_instance = self.__dict__

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        logger.info(
            "Update instance of %s from %s to %s",
            self.__tablename__,
            old_instance,
            self.__dict__,
        )

        return self.save(commit)

    def save(self, commit: bool = True):
        session.add(self)
        if commit:
            try:
                session.commit()
            except IntegrityError as exc:
                logger.error(
                    "Integrity error for %s with values %s (exc: %s)",
                    self.__tablename__,
                    self.__dict__,
                    exc,
                )
                session.rollback()
                raise
        return self

    def delete(self, commit: bool = True) -> bool:
        session.delete(self)

        logger.info("Removed instance %s of %s.", self.__dict__, self.__tablename__)

        return commit and session.commit()


class MessageQueue(Timestamp, CrudModel):
    uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid4)

    type = Column(ChoiceType(MessageType, impl=String(20)), nullable=False)

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

    history = relationship(
        "MessageQueueHistory", backref="message", cascade="all, delete-orphan"
    )
    params = relationship(
        "MessageParam", backref="message", cascade="all, delete-orphan"
    )

    def save(self, commit=True, **kwargs):
        instance = super().save(commit)

        MessageQueueHistory.create(
            **{
                "type": instance.type,
                "message_uuid": instance.uuid,
                "scheduled_to": instance.scheduled_to,
                "sender": instance.sender,
                "recipient": instance.recipient,
                "content": instance.content,
                "status": instance.status,
                "status_message": instance.status_message,
            }
        )

        return instance

    def delete(self, commit=True):
        assert (
            self.status != MessageStatus.success
        ), "You can't remove a message that was succesfully sent."

        return super().delete(commit)

    def set_status(
        self, status: MessageStatus, status_message: str = None, commit=True
    ) -> None:
        old_status = self.status
        self.update(
            **{"status": status, "status_message": status_message}, commit=commit
        )
        logger.info(
            "Updated status for %s from %s to %s, with message %s.",
            self.uuid,
            old_status,
            self.status,
            self.status_message,
        )


class MessageParam(Timestamp, CrudModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_uuid = Column(
        UUIDType(binary=False),
        ForeignKey(f"{MessageQueue.__tablename__}.uuid", ondelete="CASCADE"),
    )

    key = Column(String(100), nullable=False)
    value = Column(Text(), nullable=False)


class MessageQueueHistory(Timestamp, CrudModel):
    id = Column(Integer, primary_key=True, autoincrement=True)

    message_uuid = Column(
        UUIDType(binary=False),
        ForeignKey(f"{MessageQueue.__tablename__}.uuid", ondelete="CASCADE"),
    )
    type = Column(ChoiceType(MessageType, impl=String(20)), nullable=False)
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
