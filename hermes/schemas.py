# pylint: disable=unsubscriptable-object
from datetime import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel

from .enums import MessageType


class MessageUuidRequest(BaseModel):
    uuid: UUID


class MessageParam(BaseModel):
    param: str
    content: str


class MessageCreateRequest(BaseModel):
    type: MessageType
    scheduled_to: datetime = datetime.now()
    sender: str
    recipient: str
    content: Optional(str) = None

    params: Optional[List[MessageParam]] = []


class MessageResponse(MessageCreateRequest):
    uuid: UUID
    status: str
    status_message: Optional(str) = None
