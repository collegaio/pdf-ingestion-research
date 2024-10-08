from typing import Annotated, Optional, TypedDict
from click import Option
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

# from langgraph.checkpoint.memory import MemorySaver

from chatbot.chat.models import StudentProfile
from chatbot.pipelines.tools import make_tool_pipeline
from chatbot.pipelines.dataset import load_retrievers
from chatbot.pipelines.student import pipeline as student_pipeline
from chatbot.config.clients import (
    cohere_langchain_embed_model,
    cohere_langchain_llm,
    collega_datasets_vectorstore,
    datasets,
)


class ChatState(TypedDict):
    student_id: str
    student_profile: Optional[StudentProfile] = None
    messages: Annotated[list, add_messages]


workflow = StateGraph(ChatState)


# Define the function that calls the model
retriever_tools = load_retrievers(
    datasets=datasets,
    llm=cohere_langchain_llm,
    embed_model=cohere_langchain_embed_model,
    vector_store=collega_datasets_vectorstore,
)

DEFAULT_EXTRACT_QUESTION_PROMPT = """
Given the following user messages, extract the main question.
If there is no question, respond with "NO QUESTION".

User messages:
{messages}

Extracted question:
"""


async def determine_question(state: ChatState):
    # Filter the last 5 user messages
    # user_messages = [
    #     msg.content for msg in state["messages"][-5:] if isinstance(msg, HumanMessage)
    # ]
    user_messages = [msg.content for msg in state["messages"][-5:]]

    # Create a prompt to extract the question
    chain = (
        {"messages": RunnablePassthrough()}
        | ChatPromptTemplate.from_messages([("human", DEFAULT_EXTRACT_QUESTION_PROMPT)])
        | cohere_langchain_llm
    )

    # Generate the extraction using the LLM
    extraction = await chain.ainvoke("\n".join(user_messages))

    return {"messages": extraction.content.strip()}


def check_no_question(state: ChatState):
    last_message = state["messages"][-1]

    if not last_message or "no question" in last_message.content.lower():
        return "default"
    else:
        return "continue"


# TODO: add top 10 school creator as tool
tool_graph = make_tool_pipeline(
    tools=[],
    workflows=retriever_tools,
    llm=cohere_langchain_llm,
    embed_model=cohere_langchain_embed_model,
)


async def agent(state: ChatState):
    print("incoming agent state:", state)
    # TODO: add generalized vector search to context
    # TODO: using extracted information, determine follow up questions
    result = await cohere_langchain_llm.ainvoke(state["messages"])
    print("outgoing agent messages:", result)
    return {"messages": [result]}


workflow.add_node("extract_question", determine_question)
workflow.add_node("student_info", student_pipeline)
workflow.add_node("agent", agent)
workflow.add_node("graph", tool_graph)

workflow.add_edge(START, "student_info")
# workflow.add_edge(START, "extract_question")

workflow.add_edge("student_info", "extract_question")
workflow.add_conditional_edges(
    "extract_question", check_no_question, {"default": "agent", "continue": "graph"}
)

workflow.add_edge("graph", END)
workflow.add_edge("agent", END)

# checkpointer = MemorySaver()

app = workflow.compile()
print(app.get_graph().draw_mermaid())
