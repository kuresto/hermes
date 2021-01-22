from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .dependencies import get_db_session
from .models import MessageParam, MessageQueue
from .schemas import MessageCreateRequest, MessageResponse

messages_router = APIRouter(prefix="/messages", tags=["Messages"])


async def fetch_message(message_uuid: UUID):
    if not MessageQueue.exists(MessageQueue.uuid == message_uuid):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Message {message_uuid} not found.",
        )

    return MessageQueue.query.filter(MessageQueue.uuid == message_uuid).one()


@messages_router.get("/{message_uuid}", summary="Get message info")
async def get_message(
    message: MessageQueue = Depends(fetch_message),
    response_model=MessageResponse,
):
    return message


@messages_router.delete("/{message_uuid}", summary="Remove message from queue")
async def delete_message(message: MessageQueue = Depends(fetch_message)):
    message.delete()
    return {"message": f"Removed {message.uuid}"}


@messages_router.post("/", summary="Schedule message", status_code=HTTPStatus.CREATED)
async def create_message(
    message: MessageCreateRequest,
    session: Session = Depends(get_db_session),
    response_model=MessageResponse,
):
    message_dict = message.dict()
    params_dict = message_dict.pop("params")

    instance = MessageQueue.create(**message_dict)

    params_insert = []
    for param in params_dict:
        params_insert.append(
            MessageParam(
                message_uuid=instance.uuid, key=param["key"], value=param["value"]
            )
        )

    session.bulk_save_objects(params_insert)
    session.commit()

    return instance


@messages_router.get("/", summary="List messages (not implemented)")
async def list_messages():
    raise NotImplementedError("Not asked on the challenge.")


@messages_router.put(
    "/{message_id}", summary="Update an unsent message (not implemented)"
)
async def update_message(message_id: str):
    raise NotImplementedError("Not asked on the challenge.")
