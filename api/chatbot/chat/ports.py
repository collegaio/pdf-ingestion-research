from abc import ABC, abstractmethod
from typing import List

from chatbot.server.conversations.model import ChatHistoryMessage


class ChatMessageHandler(ABC):
    @abstractmethod
    def reply(self, message: str, chat_history: List[ChatHistoryMessage]) -> str:
        raise NotImplementedError
