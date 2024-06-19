from typing import List


from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.selectors import LLMMultiSelector
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.llms import LLM
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

from chatbot.chat.models import CDSDataset


def create_cds_query_engine(
    datasets: List[CDSDataset], llm: LLM, index: VectorStoreIndex
):
    query_engine_tools = []

    for dataset in datasets:
        query_engine = get_dataset_query_engine(
            dataset_id=dataset.id, llm=llm, index=index
        )

        tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name=dataset.id,
                description=(dataset.description),
            ),
        )

        query_engine_tools.append(tool)

    return RouterQueryEngine(
        selector=LLMMultiSelector.from_defaults(llm=llm),
        query_engine_tools=query_engine_tools,
        verbose=True,
    )

    # return QueryEngineTool.from_defaults(
    #     query_engine=cds_query_engine,
    #     name="cds_query_engine",
    #     description="Answers questions about admissions data from 2023 onward such as GPA, standardized test scores, demographic data, and financial aid award sizes",
    # )


def get_dataset_query_engine(dataset_id: str, llm: LLM, index: VectorStoreIndex):
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
