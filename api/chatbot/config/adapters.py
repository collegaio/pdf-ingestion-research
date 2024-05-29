from chatbot.adapters.cohere import CohereChatAdapter
from chatbot.config.env import COHERE_API_KEY


chat_handler = CohereChatAdapter(COHERE_API_KEY)
