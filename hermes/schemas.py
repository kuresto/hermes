# pylint: disable=unsubscriptable-object,no-name-in-module
from datetime import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel

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


class MessageResponse(MessageCreateRequest):
    uuid: UUID
    status: str
    status_message: Optional[str] = None

    class Config:
        orm_mode = True
