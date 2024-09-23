from typing import List

from langchain_core.messages import HumanMessage, SystemMessage

from chatbot.server.conversations.model import ChatHistoryMessage
from chatbot.pipelines.chat import app


async def handle_message(
    message: str,
    chat_history: List[ChatHistoryMessage],
):
    system_prompt = """
    You are a high school guidance counselor who is trying to help students.
    Disuade the student if they are not qualified for what they are asking.
    Always give an answer even if the supporting context is not relevant.
    """

    final_state = await app.ainvoke(
        {
            "messages": [SystemMessage(content=system_prompt)]
            + [message.to_langchain_message() for message in chat_history]
            + [HumanMessage(content=message)]
        },
    )

    print(
        "last messages:",
        [msg.content for msg in final_state["messages"][-5:]],
    )
    # assert final_state["messages"][-1] is None
    return final_state["messages"][-1].content
