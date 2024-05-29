from typing import List

from llama_index.llms.cohere import Cohere
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.llms import ChatMessage

from chatbot.chat.ports import ChatMessageHandler


class CohereChatAdapter(ChatMessageHandler):
    def __init__(self, api_key: str) -> None:
        self.llm = Cohere(model="command-r-plus", api_key=api_key)

    def reply(self, message: str, chat_history: List[str]) -> str:
        # TODO: differentiate message_role for history (user, system, assistant)
        chat_memory = ChatMemoryBuffer.from_defaults(
            chat_history=[ChatMessage.from_str(msg) for msg in chat_history],
            llm=self.llm,
        )

        chat_engine = SimpleChatEngine.from_defaults(llm=self.llm, memory=chat_memory)

        return chat_engine.chat(message).response
