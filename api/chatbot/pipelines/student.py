import json
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from pydantic import BaseModel

from chatbot.adapters.api import get_student_profile, update_student_profile
from chatbot.config.clients import cohere_langchain_llm
from chatbot.chat.models import StudentProfile


class InfoExtractionState(TypedDict):
    student_id: str
    messages: Annotated[list, add_messages]
    student_profile: StudentProfile


def get_field_descriptions(cls: BaseModel):
    return [f"{field}" for field in cls.__annotations__]


async def extract_student_info(state: InfoExtractionState):
    """
    Extracts student information from a conversation.

    Args:
        state (InfoExtractionState): The current state of the conversation.

    Returns:
        InfoExtractionState: The updated state with the extracted student information.
    """
    # Create a parser for the StudentProfile
    # parser = PydanticOutputParser(pydantic_object=StudentProfile)
    parser = JsonOutputParser(pydantic_object=StudentProfile)

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"You are an AI assistant tasked with extracting student information from a conversation. "
                f"Extract the following information if available: {', '.join(get_field_descriptions(StudentProfile))}. "
                f"If a piece of information is not provided, leave it as null.",
            ),
            ("human", "Here's the conversation history:"),
            ("human", "{conversation}"),
            (
                "human",
                "Please extract the student information and format it as follows:",
            ),
            ("human", "{format_instructions}"),
        ],
    )

    # Prepare the conversation history
    conversation = "\n".join(
        [
            f"{'Human' if isinstance(msg, HumanMessage) else 'AI'}: {msg.content}"
            for msg in state["messages"]
        ]
    )

    # Create the full prompt
    full_prompt = prompt.format_messages(
        conversation=conversation,
        format_instructions=parser.get_format_instructions(),
        # format_instructions=StudentProfile.model_json_schema(),
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

        # Extract the properties from the nested structure
        extracted_info = parsed_response.get("properties", {})

        # Create StudentProfile object
        extracted_info["student_id"] = state["student_id"]
        student_profile = StudentProfile(**extracted_info)

        # Return the updated state with the extracted StudentProfile
        return {
            "messages": state["messages"],
            "student_profile": student_profile,
        }
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {
            "messages": state["messages"]
            + [AIMessage(content="Error extracting student information.")],
            "student_profile": None,
        }


def update_student_info(state: InfoExtractionState):
    """
    Fetches the student info, merges with the new info, and returns the student
    Only sets fields that were originally null

    Args:
        state (InfoExtractionState): The current state of the conversation.

    Returns:
        InfoExtractionState: The updated state with the provided information.
    """
    print("parsed student profile:", state["student_profile"])
    current_student_profile = get_student_profile(state["student_id"])
    print("current student profile:", current_student_profile)

    for field, value in state["student_profile"]:
        if getattr(current_student_profile, field) is None:
            setattr(current_student_profile, field, value)

    update_student_profile(state["student_id"], current_student_profile)

    print("outgoing update_student_info state:", current_student_profile)
    student_info_message = SystemMessage(
        content=f"Student Profile: {current_student_profile}"
    )
    return {
        "student_profile": current_student_profile,
        # "messages": state["messages"] + [student_info_message]
        "messages": [student_info_message],
    }


### Workflow

workflow = StateGraph(InfoExtractionState)

workflow.add_node("extract_student_info", extract_student_info)
workflow.add_node("update_student_info", update_student_info)

workflow.add_edge(START, "extract_student_info")
workflow.add_edge("extract_student_info", "update_student_info")
workflow.add_edge("update_student_info", END)

pipeline = workflow.compile()
