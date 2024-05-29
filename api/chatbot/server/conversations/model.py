from typing import List

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    chat_history: List[str]
