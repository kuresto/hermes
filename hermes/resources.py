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


@messages_router.get(
    "/{message_uuid}", summary="Get message info", response_model=MessageResponse
)
async def get_message(message: MessageQueue = Depends(fetch_message)):
    return message


@messages_router.delete(
    "/{message_uuid}",
    summary="Remove message from queue",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_message(message: MessageQueue = Depends(fetch_message)):
    try:
        message.delete()
    except AssertionError as exc:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return {}


@messages_router.post(
    "/",
    summary="Schedule message",
    status_code=HTTPStatus.CREATED,
    response_model=MessageResponse,
)
async def create_message(
    message: MessageCreateRequest, session: Session = Depends(get_db_session)
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
async def update_message(message_id: UUID):
    raise NotImplementedError("Not asked on the challenge.")
