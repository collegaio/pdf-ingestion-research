from abc import ABC, abstractmethod
from typing import List


class ChatMessageHandler(ABC):
    @abstractmethod
    def reply(self, message: str, chat_history: List[str]) -> str:
        raise NotImplementedError
