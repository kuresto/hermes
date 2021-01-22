# pylint: disable=unsubscriptable-object,no-name-in-module,no-self-argument
from datetime import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, validator

from .enums import MessageType


class MessageParam(BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True


class MessageCreateRequest(BaseModel):
    type: MessageType
    scheduled_to: datetime = datetime.now()
    sender: str
    recipient: str
    content: Optional[str] = None

    params: Optional[List[MessageParam]] = []

    class Config:
        orm_mode = True

    @validator("scheduled_to")
    def validate_if_date_bigger_than_today(cls, value):
        assert (
            value < datetime.utcnow()
        ), "You can only schedule a message now or for the future"

        return value


class MessageResponse(MessageCreateRequest):
    uuid: UUID
    status: str
    status_message: Optional[str] = None

    class Config:
        orm_mode = True
