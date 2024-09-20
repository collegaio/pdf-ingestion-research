from typing import List


from llama_index.core.tools import QueryEngineTool, ToolMetadata, RetrieverTool
from llama_index.core.selectors import PydanticMultiSelector
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.retrievers import RouterRetriever
from llama_index.core.llms import LLM
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

from chatbot.chat.models import Dataset


def load_retrievers(datasets: List[Dataset], llm: LLM, index: VectorStoreIndex):
    retrievers = []

    for dataset in datasets:
        retriever = create_dataset_retriever(dataset=dataset, llm=llm, index=index)

        # out = retriever.call()
        # out.content

        retrievers.append(retriever)

    return retrievers


def create_dataset_retriever(dataset: Dataset, llm: LLM, index: VectorStoreIndex):
    retriever_tools = []

    for datapoint in dataset.datapoints:
        query_engine = get_dataset_retriever(
            dataset_id=datapoint.id, llm=llm, index=index
        )

        tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name=datapoint.id,
                description=(datapoint.description),
            ),
        )
        # tool = RetrieverTool(
        #     retriever=query_engine,
        #     metadata=ToolMetadata(
        #         name=dataset.id,
        #         description=(dataset.description),
        #     ),
        # )

        retriever_tools.append(tool)

    for nested_dataset in dataset.datasets:
        tool = create_dataset_retriever(nested_dataset, llm=llm, index=index)

        retriever_tools.append(tool)

    # return RouterQueryEngine(
    #     selector=LLMMultiSelector.from_defaults(llm=llm),
    #     query_engine_tools=query_engine_tools,
    #     verbose=True,
    # )
    # return RouterRetriever(
    #     selector=PydanticMultiSelector.from_defaults(llm=llm),
    #     retriever_tools=retriever_tools,
    #     verbose=True,
    # )
    dataset_query_engine = RouterQueryEngine.from_defaults(
        query_engine_tools=retriever_tools,
        llm=llm,
        selector=PydanticMultiSelector.from_defaults(llm=llm),
    )

    return QueryEngineTool.from_defaults(
        query_engine=dataset_query_engine,
        name=dataset.name,
        description=dataset.description,
    )


def get_dataset_retriever(dataset_id: str, llm: LLM, index: VectorStoreIndex):
    vector_filter = MetadataFilters(
        filters=[
            MetadataFilter(
                key="dataset_id",
                operator=FilterOperator.EQ,
                value=dataset_id,
            ),
        ]
    )

    return index.as_query_engine(
        llm=llm,
        verbose=True,
        filters=vector_filter,
    )
    # return index.as_retriever(
    #     llm=llm,
    #     verbose=True,
    #     filters=vector_filter,
    # )
