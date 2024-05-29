from typing import List
from chatbot.chat.ports import ChatMessageHandler


def handle_message(
    message: str, chat_history: List[str], chat_handler: ChatMessageHandler
):
    return chat_handler.reply(message, chat_history)
