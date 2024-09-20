from typing import Annotated, Dict, List, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


class State(TypedDict):
    messages: Annotated[list, add_messages]
    selected_tools: list[str]
    selected_workflows: list[str]


class Workflow(TypedDict):
    name: str
    description: str
    workflow: CompiledStateGraph


def make_tool_selector(tool_vectorstore: VectorStore):
    async def select_tools(state: State):
        # TODO: determine question from all messages
        last_user_message = state["messages"][-1]

        query = last_user_message.content

        tool_documents = await tool_vectorstore.asimilarity_search_with_score(
            query, k=1
        )

        selected = {
            "selected_tools": [],
            "selected_workflows": [],
        }

        for doc, _ in tool_documents:
            if "workflow_name" in doc.metadata:
                selected["selected_workflows"].append(doc.id)
            elif "tool_name" in doc.metadata:
                selected["selected_tools"].append(doc.id)

        return selected

    return select_tools


def make_agent(llm: BaseChatModel, tools: List[BaseTool]):
    async def agent(state: State):
        llm_with_tools = llm.bind_tools(
            [tool for tool in tools if tool.name in state["selected_tools"]]
        )

        return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}

    return agent


def choose_next_nodes(state: State):
    nodes = []

    if state["selected_tools"] != []:
        nodes.append("agent")

    for workflow in state["selected_workflows"]:
        nodes.append(workflow)

    return nodes


def make_tool_pipeline(
    tools: List[BaseTool],
    workflows: List[Workflow],
    llm: BaseChatModel,
    embed_model: Embeddings,
):
    workflow = StateGraph(State)

    tool_node = ToolNode(tools=tools)
    tool_vectorstore = InMemoryVectorStore(embed_model)

    tool_vectorstore.add_documents(
        [
            Document(
                id=tool.name,
                page_content=tool.description,
                metadata={"tool_name": tool.name},
            )
            for tool in tools
        ]
    )

    tool_vectorstore.add_documents(
        [
            Document(
                id=nested_workflow["name"],
                page_content=nested_workflow["description"],
                metadata={"workflow_name": nested_workflow["name"]},
            )
            for nested_workflow in workflows
        ]
    )

    workflow.add_node("agent", make_agent(llm=llm, tools=tools))
    workflow.add_node("select_tools", make_tool_selector(tool_vectorstore))
    workflow.add_node("tools", tool_node)

    for nested_workflow in workflows:
        workflow.add_node(nested_workflow["name"], nested_workflow["workflow"])
        # workflow.add_edge(nested_workflow["name"], END)

    workflow.add_edge(START, "select_tools")
    workflow.add_conditional_edges(
        "select_tools",
        choose_next_nodes,
        {
            "agent": "agent",
            **{
                nested_workflow["name"]: nested_workflow["name"]
                for nested_workflow in workflows
            },
        },
    )
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
    )
    workflow.add_edge("tools", "agent")

    # checkpointer = MemorySaver()
    return workflow.compile()


def make_tool_pipeline_acaller(pipeline: CompiledStateGraph):
    async def acall_tool_pipeline(message: str):
        return await pipeline.ainvoke(
            {"messages": [HumanMessage(content=message)]},
        )

    return acall_tool_pipeline