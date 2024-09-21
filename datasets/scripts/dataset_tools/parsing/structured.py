from typing import Any, List, Literal

from llama_index.core.llms import LLM
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.indices import VectorStoreIndex
from llama_index.core import PromptTemplate
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
from pydantic import BaseModel, Field


class Column(BaseModel):
    name: str = Field(description="Column name")
    possible_values: List[str | int | float] | None = Field(
        description="Possible values for this column", default=None
    )
    datatype: Literal["string", "integer", "number", "boolean"] = Field(
        description="JSON Datatype of values for column"
    )


def columns_to_schema(columns: List[Column]):
    return {
        "title": "Fields",
        "type": "object",
        "properties": {
            column.name: {
                "title": column.name,
                "type": "object",
                "properties": {
                    "value": {
                        "anyOf": [{"type": column.datatype}, {"type": "null"}],
                        "default": None,
                        "title": "value",
                        **(
                            {
                                "enum": (
                                    [True, False] + [None]
                                    if "boolean" == column.datatype
                                    else column.possible_values + [None]
                                )
                            }
                            if column.possible_values is not None
                            or "boolean" == column.datatype
                            else {}
                        ),
                    },
                    "explanation": {"title": "explanation", "type": "string"},
                },
            }
            for column in columns
        },
    }


EXTRACT_INFO_TEMPLATE = PromptTemplate(
    template="""
    Here is some text from a document:

    {text}

    Provide values for following fields using this JSON schema:

    {schema}

    Only output properly formatted JSON.
    Set the value as null if it can't be inferred from the text.
    Do not include commas, "$", or "%" in numbers.
"""
)

VALUE_VALID_TEMPLATE = PromptTemplate(
    template="""
    Here is some text from a document:

    {text}

    Verify that the following key value pair is correct.

    {column_name}: {value}

    Output "TRUE" or "FALSE" and give an explanation.
    If the text does not contain a value for {column_name} and the value is "None", output "TRUE".
    If "FALSE", also return properly formatted JSON with the correct value in "key_name: value" format.
"""
)

# EXTRACT_KEY_VALUES_TEMPLATE = PromptTemplate(
#     template="""
# Represent the following as a dataframe of key,value pairs.
# Use snake_case for the key names.
# For dollar ($) or percent (%) values, parse them as a float with the word "dollars" or "percent" in the key name
# Do not include commas (,) in numeric values, parse them as an int or float.
# Do not make up pairs or examples that are not in the text.

# {text}
# """
# )

EXTRACT_KEY_VALUES_TEMPLATE = PromptTemplate(
    template="""
    Here is some text from a document:

    {text}

    Extract key: value pairs from the text as a markdown list.

    The list should be in the following format:

    # Subject

    * key_name: value
    * key_name: value
    ...

    Use snake_case for the key names.
    Key names should be unique in the list. Do not repeat keys.
    Each value should be a string, int, float, or boolean.
    For dollar ($) or percent (%) values, parse them as a float with the word "dollars" or "percent" in the key name.
    If the value is a date, give the date in ISO format as YYYY-MM-DD.
    Do not create nested lists or as values.
    Do not make up pairs or examples that are not in the text.
"""
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
