from tabnanny import verbose
from typing import List

from llama_index.llms.cohere import Cohere
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import BaseTool
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.llms import ChatMessage
from marshmallow import pre_dump

from chatbot.server.conversations.model import ChatHistoryMessage
from chatbot.chat.ports import ChatMessageHandler


class CohereChatAdapter(ChatMessageHandler):
    def __init__(self, api_key: str, query_tools: List[BaseTool]) -> None:
        self.llm = Cohere(model="command-r-plus", api_key=api_key)
        self.query_tools = query_tools
        self.context = """
        Answer questions like you are Mark Cuban who has become a high school guidance counselor.
        Never say "I am Mark Cuban" or identify yourself though.
        Disuade the student if they are not qualified for what they are asking.
        """

    def reply(self, message: str, chat_history: List[ChatHistoryMessage]) -> str:
        chat_engine = ReActAgent.from_tools(
            tools=self.query_tools,
            llm=self.llm,
            chat_history=[
                ChatMessage.from_str(msg.text, role=str(msg.role.value).lower())
                for msg in chat_history
            ],
            context=self.context,
            verbose=True,
        )

        return chat_engine.chat(message).response
