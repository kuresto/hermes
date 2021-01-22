from fastapi import APIRouter

from .schemas import MessageUuidRequest, MessageCreateRequest


messages_router = APIRouter()


@messages_router.get("/messages/{message_uuid}", tags=["messages"])
async def get_message(message_uuid: MessageUuidRequest):
    pass


@messages_router.delete("/messages/{message_uuid}", tags=["messages"])
async def delete_message(message_id: MessageUuidRequest):
    pass


@messages_router.post("/messages/", tags=["messages"])
async def create_message(message: MessageCreateRequest):
    pass


@messages_router.post("/messages/", tags=["messages"])
async def list_messages():
    raise NotImplementedError("Not asked on the challenge.")


@messages_router.put("/messages/{message_id}", tags=["messages"])
async def update_message(message_id: MessageUuidRequest):
    raise NotImplementedError("Not asked on the challenge.")
