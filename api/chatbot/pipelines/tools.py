import json
from typing import Annotated, List, TypedDict

from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import BaseTool
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from chatbot.config.clients import cohere_langchain_llm

class State(TypedDict):
    # student_id: str
    # student_profile: StudentProfile
    messages: Annotated[list, add_messages]
    selected_tool: str | None
    selected_workflow: str | None


class Workflow(TypedDict):
    name: str
    description: str
    workflow: CompiledStateGraph


class ToolSelectionOutput(BaseModel):
    selected_tool_id: str = Field(description="The id of the selected tool")


async def pick_tool(tool_documents: List[Document], query: str):
    parser = JsonOutputParser(pydantic_object=ToolSelectionOutput)

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given the following tools and query, select the most relevant tool to answer the query.",
            ),
            ("human", "Query: {query}"),
            ("human", "Tools: {tool_documents}"),
            (
                "human",
                "Return the id of the selected tool in JSON format according to the following schema:",
            ),
            ("human", "{format_instructions}"),
        ],
    )

    # Create the full prompt
    full_prompt = prompt.format_messages(
        query=query,
        tool_documents="\n".join(
            [f"{doc.id}: {doc.page_content}" for doc in tool_documents]
        ),
        # format_instructions=ToolSelectionOutput.model_json_schema(),
        format_instructions=parser.get_format_instructions(),
    )

    # Invoke the LLM
    llm_response = await cohere_langchain_llm.ainvoke(full_prompt)
    print("llm_response:", llm_response)

    # Parse the LLM output
    # json_start = llm_response.content.find("{")
    # json_end = llm_response.content.rfind("}") + 1
    # json_str = llm_response.content[json_start:json_end]

    try:
        parsed_response = parser.parse(llm_response.content)
        print("parsed_response:", parsed_response)

        # Extract the properties from the nested structure
        tool_selection = ToolSelectionOutput(**parsed_response)

        return next((doc for doc in tool_documents if doc.id == tool_selection.selected_tool_id), None)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def make_tool_selector(tool_vectorstore: VectorStore):
    async def select_tools(state: State):
        last_user_message = state["messages"][-1]

        query = last_user_message.content
        print("query:", query)
        # TODO: use LLM to get subject from query
        tool_documents = await tool_vectorstore.asimilarity_search(
            query,
            k=2,
            debug=False,
            verbose=False,
        )

        print("tool_documents:", tool_documents)
        # tool_documents: [Document(id='guide_to_college_admissions', metadata={'tool_name': 'guide_to_college_admissions'}, page_content='guide_to_college_admissions')]
        selected = {
            "selected_tool": None,
            "selected_workflow": None,
        }

        selected_tool = await pick_tool(tool_documents, query)

        if selected_tool:
            if "workflow_name" in selected_tool.metadata:
                selected["selected_workflow"] = selected_tool.metadata["workflow_name"]
            elif "tool_name" in selected_tool.metadata:
                selected["selected_tool"] = selected_tool.metadata["tool_name"]

        return selected

    return select_tools


def make_agent(llm: BaseChatModel, tools: List[BaseTool]):
    async def agent(state: State):
        print("graph state:", state)
        llm_with_tools = llm.bind_tools(
            [tool for tool in tools if tool.name == state["selected_tool"]]
        )

        result = await llm_with_tools.ainvoke(state["messages"])
        print("outgoing graph messages:", result)
        return {"messages": [result]}

        # return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}

    return agent


def choose_next_nodes(state: State):
    # NOTE: can only select one tool or workflow at a time
    nodes = []

    if state["selected_workflow"]:
        nodes.append(state["selected_workflow"])
    elif state["selected_tool"]:
        nodes.append("agent")

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

    # add tool descriptions to vector store
    # TODO: add possible questions as documents
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

    # add workflow descriptions as tools to vector store
    # TODO: add possible questions as documents
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


# def make_tool_pipeline_acaller(pipeline: CompiledStateGraph):
#     async def acall_tool_pipeline(message: str):
#         return await pipeline.ainvoke(
#             {"messages": [HumanMessage(content=message)]},
#         )

#     return acall_tool_pipeline
