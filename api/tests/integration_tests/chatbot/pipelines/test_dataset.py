from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.messages import ToolCall

import pytest

from chatbot.config.clients import cohere_langchain_llm, cohere_langchain_embed_model
from chatbot.chat.models import Datapoint
from chatbot.pipelines.dataset import get_dataset_retriever


@pytest.mark.asyncio
async def test_dataset_retriever_tool():
    datapoint = Datapoint(id="test", description="basic retriever")
    vector_store = InMemoryVectorStore(embedding=cohere_langchain_embed_model)

    vector_store.as_retriever()

    await vector_store.aadd_documents(
        [
            Document(
                page_content="the weather in SF is 85 degrees",
                metadata={"dataset_id": "test"},
            )
        ]
    )

    retriever_tool = get_dataset_retriever(
        datapoint=datapoint,
        llm=cohere_langchain_llm,
        vector_store=vector_store,
    )

    result = await retriever_tool.ainvoke("What is the weather in san francisco?")
    assert result is None
