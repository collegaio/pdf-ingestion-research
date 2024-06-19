from typing import List
from urllib import response


from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.tools import QueryEngineTool, FunctionTool

from chatbot.chat.query_engine import create_cds_query_engine
from chatbot.adapters import college_scorecard
from chatbot.config import clients
from chatbot.chat.agent import create_chat_agent, create_chat_agent_query_pipeline
from chatbot.chat.models import CDSDataset
from chatbot.server.conversations.model import ChatHistoryMessage
from chatbot.chat.ports import ChatMessageHandler
from chatbot.pipelines.chances import create_chances_query_chain


cds_query_engine = create_cds_query_engine(
    datasets=clients.datasets.cds_files,
    llm=clients.gpt_llm,
    index=clients.pinecone_adapter.get_index(
        "cds-index-test", embed_model=clients.gpt_embedding_model
    ),
)

chances_query_chain = create_chances_query_chain(
    llm=clients.gpt_llm, cds_query_engine=cds_query_engine
)


def determine_chances(query_str: str, chat_history: List[str]):
    response = chances_query_chain.run(
        input=query_str,
        chat_history=chat_history,
    )

    return response


async def adetermine_chances(query_str: str, chat_history: List[str]):
    response = await chances_query_chain.arun(
        input=query_str,
        chat_history=chat_history,
    )

    return response


# 'system', 'assistant', 'user', 'function', and 'tool'

agent_query_pipeline = create_chat_agent_query_pipeline(
    llm=clients.cohere_llm,
    context="""
    Answer questions like you are Mark Cuban who has become a high school guidance counselor.
    Never say "I am Mark Cuban" or identify yourself though.
    Disuade the student if they are not qualified for what they are asking.
    """,
    tools=[
        QueryEngineTool.from_defaults(
            query_engine=cds_query_engine,
            name="cds_query_engine",
            description="Answers questions about admissions data from 2023 onward such as GPA, standardized test scores, demographic data, and financial aid award sizes",
        ),
        FunctionTool.from_defaults(
            determine_chances,
            async_fn=adetermine_chances,  # optional!
        ),
        college_scorecard.college_lookup_tool,
    ],
)


async def handle_message(
    message: str,
    chat_history: List[ChatHistoryMessage],
):
    # return chat_handler.reply(message, chat_history)
    # create chat agent
    chat_agent = create_chat_agent(
        agent_query_pipeline,
        # chat_history=[],
        chat_history=[
            ChatMessage.from_str(
                msg.text,
                role=(
                    MessageRole.ASSISTANT
                    if (role := str(msg.role.value).lower()) == "chatbot"
                    else role
                ),
            )
            for msg in chat_history
        ],
    )

    result = await chat_agent.achat(message)

    return result.response
