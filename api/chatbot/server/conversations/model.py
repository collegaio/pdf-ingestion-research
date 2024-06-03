from enum import Enum
from re import L
from typing import List

from pydantic import BaseModel


class ChatMessageRole(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
    CHATBOT = "CHATBOT"


class ChatHistoryMessage(BaseModel):
    text: str
    role: ChatMessageRole


class ChatRequest(BaseModel):
    message: str
    chat_history: List[ChatHistoryMessage]
