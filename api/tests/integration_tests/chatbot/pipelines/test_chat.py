# from langchain_aws import BedrockLLM
from langchain_aws import ChatBedrockConverse, BedrockEmbeddings
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from langchain_core.vectorstores.in_memory import InMemoryVectorStore
import pytest
import boto3

from chatbot.pipelines.chat import app
from chatbot.config.clients import collega_datasets_vectorstore


@pytest.mark.asyncio
async def test_chat_pipeline():
    # Use the Runnable
    final_state = await app.ainvoke(
        # {"messages": [HumanMessage(content="what is the weather in sf")]},
        {
            "messages": [
                HumanMessage(content="Stanford is a university in california"),
                HumanMessage(content="what is the average gpa at that school?"),
            ]
        },
        # config={"configurable": {"thread_id": 42}}
    )

    print("messages:", final_state["messages"])
    assert final_state["messages"][-1] is None


@pytest.mark.asyncio
async def test_embedding():
    bedrock_client = boto3.client("bedrock-runtime")
    embeddings = BedrockEmbeddings(
        model_id="cohere.embed-english-v3", client=bedrock_client
    )

    document_1 = Document(id="1", page_content="the president", metadata={"baz": "bar"})
    vector_store = InMemoryVectorStore(embeddings)

    doc_embedding = await vector_store.aadd_documents([document_1])
    print(doc_embedding)
    found_docs = vector_store.similarity_search_with_score(query="the presidentt", k=1)
    print(found_docs)
    assert False


@pytest.mark.asyncio
async def test_vector_search():
    docs = collega_datasets_vectorstore.similarity_search_with_score(
        "What is the average GPA at johns hopkins?",
        k=4,
    )
    print(docs)
    assert collega_datasets_vectorstore is None
