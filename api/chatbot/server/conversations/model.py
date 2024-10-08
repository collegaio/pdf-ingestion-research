from enum import Enum
from re import L
from typing import List

from pydantic import BaseModel

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class ChatMessageRole(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
    CHATBOT = "CHATBOT"


class ChatHistoryMessage(BaseModel):
    text: str
    role: ChatMessageRole

    def to_langchain_message(self):
        if self.role == ChatMessageRole.CHATBOT:
            return AIMessage(content=self.text)
        elif self.role == ChatMessageRole.SYSTEM:
            return SystemMessage(content=self.text)
        else:
            return HumanMessage(content=self.text)


class ChatRequest(BaseModel):
    student_id: str
    message: str
    chat_history: List[ChatHistoryMessage]
