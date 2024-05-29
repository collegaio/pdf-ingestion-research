from fastapi import APIRouter

from chatbot.server.conversations.model import ChatRequest
from chatbot.chat import llm
from chatbot.config.adapters import chat_handler

router = APIRouter()


@router.post("/chat")
async def read_user(body: ChatRequest):
    response = llm.handle_message(
        message=body.message,
        chat_history=body.chat_history,
        chat_handler=chat_handler,
    )

    return {"message": response}
