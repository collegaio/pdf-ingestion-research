from fastapi import APIRouter

from chatbot.server.conversations.model import ChatRequest
from chatbot.chat import llm

router = APIRouter()


@router.post("/chat")
async def read_user(body: ChatRequest):
    response = await llm.handle_message(
        student_id=body.student_id,
        message=body.message,
        chat_history=body.chat_history,
    )

    return {"message": response}
