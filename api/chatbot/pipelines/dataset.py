from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import StructuredTool, BaseTool
from langgraph.graph.state import CompiledStateGraph

from chatbot.pipelines.tools import make_tool_pipeline
from chatbot.chat.models import Datapoint, Dataset

DEFAULT_QUESTION_ANSWERING_TEMPLATE = """
Answer the user's questions based on the below context. 
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

{question}

Context:
{context}
"""


def load_retrievers(
    datasets: List[Dataset],
    llm: BaseChatModel,
    embed_model: Embeddings,
    vector_store: VectorStore,
):
    # tools: List[StructuredTool] = []
    pipelines = []

    for dataset in datasets:
        pipeline = create_dataset_retriever(
            dataset=dataset,
            llm=llm,
            embed_model=embed_model,
            vector_store=vector_store,
        )

        # tool = StructuredTool.from_function(
        #     coroutine=make_tool_pipeline_acaller(pipeline),
        #     name=dataset.name,
        #     description=dataset.description,
        # )

        # tools.append(tool)
        pipelines.append(
            {
                "name": dataset.name,
                "description": dataset.description,
                "workflow": pipeline,
            }
        )

    # return tools
    return pipelines


# TODO: test creates correct amount of retrievers and nested retrievers
def create_dataset_retriever(
    dataset: Dataset,
    llm: BaseChatModel,
    embed_model: Embeddings,
    vector_store: VectorStore,
):
    retriever_tools: List[BaseTool | CompiledStateGraph] = []
    nested_workflows = []

    for datapoint in dataset.datapoints:
        tool = get_dataset_retriever(
            datapoint=datapoint, llm=llm, vector_store=vector_store
        )

        retriever_tools.append(tool)

    for nested_dataset in dataset.datasets:
        nested_pipeline = create_dataset_retriever(
            nested_dataset, llm=llm, embed_model=embed_model
        )

        nested_workflows.append(
            {
                "name": nested_dataset.name,
                "description": nested_dataset.description,
                "workflow": nested_pipeline,
            }
        )

    return make_tool_pipeline(
        tools=retriever_tools,
        workflows=nested_workflows,
        llm=llm,
        embed_model=embed_model,
    )


# TODO: test retrieval
def get_dataset_retriever(
    datapoint: Datapoint, llm: BaseChatModel, vector_store: VectorStore
):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"filter": {"dataset_id": datapoint.id}},
    )

    async def query_tool(query: str) -> str:
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | ChatPromptTemplate.from_messages(
                [("human", DEFAULT_QUESTION_ANSWERING_TEMPLATE)]
            )
            | llm
        )

        return chain.invoke(query).content

    return StructuredTool.from_function(
        coroutine=query_tool,
        name=datapoint.id,
        description=datapoint.description,
    )
