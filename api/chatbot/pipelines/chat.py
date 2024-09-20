from typing import Annotated, TypedDict
from argon2 import extract_parameters
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import StructuredTool
from langchain_core.documents import Document
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# from langgraph.checkpoint.memory import MemorySaver

from chatbot.pipelines.tools import make_tool_pipeline
from chatbot.pipelines.dataset import load_retrievers
from chatbot.config.clients import (
    cohere_langchain_embed_model,
    cohere_langchain_llm,
    collega_datasets_vectorstore,
    datasets,
)


class ChatState(TypedDict):
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


tool_graph = make_tool_pipeline(
    tools=[],
    workflows=retriever_tools,
    llm=cohere_langchain_llm,
    embed_model=cohere_langchain_embed_model,
)


async def agent(state: ChatState):
    print("state:", state)
    return {"messages": [await cohere_langchain_llm.ainvoke(state["messages"])]}


workflow.add_node("extract_question", determine_question)
workflow.add_node("agent", agent)
workflow.add_node("graph", tool_graph)

workflow.add_conditional_edges(
    "extract_question", check_no_question, {"default": "agent", "continue": "graph"}
)

workflow.add_edge(START, "extract_question")

# # checkpointer = MemorySaver()

app = workflow.compile()
