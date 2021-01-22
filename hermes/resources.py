from fastapi import APIRouter

from .schemas import MessageUuidRequest, MessageCreateRequest


messages_router = APIRouter(prefix="/messages", tags=["Messages"])


@messages_router.get("/{message_uuid}", summary="Get message info")
async def get_message(message_uuid: str):
    return {"message": "ok"}


@messages_router.delete("/{message_uuid}", summary="Remove message from queue")
async def delete_message(message_id: str):
    return {"message": "ok"}


@messages_router.post("/")
async def create_message(message: MessageCreateRequest, summary="Schedule message"):
    return {"message": "ok"}


@messages_router.get("/", summary="List messages (not implemented)")
async def list_messages():
    raise NotImplementedError("Not asked on the challenge.")


@messages_router.put(
    "/{message_id}", summary="Update an unsent message (not implemented)"
)
async def update_message(message_id: str):
    raise NotImplementedError("Not asked on the challenge.")
