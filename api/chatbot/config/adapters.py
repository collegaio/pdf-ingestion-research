from chatbot.adapters.cohere import CohereChatAdapter
from chatbot.config.env import COHERE_API_KEY
from chatbot.adapters.college_scorecard import college_lookup_tool


chat_handler = CohereChatAdapter(
    api_key=COHERE_API_KEY,
    query_tools=[college_lookup_tool],
)
