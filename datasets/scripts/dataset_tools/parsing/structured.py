from typing import Any

from llama_index.core.llms import LLM
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)


async def query_structured_output(
    query: str, dataset_id: str, index: VectorStoreIndex, llm: LLM, output_cls: Any
):
    vector_filter = MetadataFilters(
        filters=[
            MetadataFilter(
                key="dataset_id",
                operator=FilterOperator.EQ,
                value=dataset_id,
            ),
        ]
    )

    query_engine = index.as_query_engine(
        llm=llm,
        verbose=True,
        filters=vector_filter,
        response_mode="compact_accumulate",
        output_cls=output_cls,
    )

    response = await query_engine.aquery(query)
    print(response)

    prompt_template_str = """\
    Generate an {cls_name}, from this string: \
    {cls_str}\
    """

    program = LLMTextCompletionProgram.from_defaults(
        llm=llm,
        output_cls=output_cls,
        prompt_template_str=prompt_template_str,
        verbose=True,
    )

    return await program.acall(cls_name=output_cls.__name__, cls_str=str(response))
