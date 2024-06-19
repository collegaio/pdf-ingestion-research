import asyncio
import json
import os
from typing import List
import dotenv

from pinecone import Pinecone, ServerlessSpec

from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.core.schema import BaseNode
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.llms import LLM
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.node_parser import MarkdownNodeParser, MarkdownElementNodeParser
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.llms.openai import OpenAI

from dataset_tools.cds.models import CDSDataset

dotenv.load_dotenv("../.env")


openai_api_key = os.environ["OPENAI_API_KEY"]
pinecone_api_key = os.environ["PINECONE_API_KEY"]

pinecone_index_name = "cds-index-test"


async def upload_dataset_to_vectorstore(
    input_dir,
    dataset: CDSDataset,
    storage_context: StorageContext,
    embed_model: BaseEmbedding,
):
    reader = SimpleDirectoryReader(
        input_files=[os.path.join(input_dir, f"{dataset.id}.md")],
    )

    documents = await reader.aload_data()

    for document in documents:
        # TODO: parser for XLSX format (it is just gibberish)
        document.doc_id = dataset.id
        document.metadata["dataset_id"] = dataset.id
        document.metadata["dataset_group"] = "cds-data"

    pipeline = IngestionPipeline(transformations=[MarkdownNodeParser()])
    nodes = await pipeline.arun(documents=documents)

    # TODO: delete vectors for this dataset_id in the vectorstore index

    return VectorStoreIndex(
        nodes=nodes, storage_context=storage_context, embed_model=embed_model
    )


async def main():
    pc = Pinecone(api_key=pinecone_api_key)
    print("existing indexes:", pc.list_indexes())

    if pinecone_index_name in (index["name"] for index in pc.list_indexes()):
        pc_index = pc.Index(pinecone_index_name)

        # if pc_index.describe_index_stats()['total_vector_count'] > 0:
        #     pc_index.delete(ids=[vector_id for vector_id in pc_index.list()], namespace="")
    else:
        pc.create_index(
            name=pinecone_index_name,
            dimension=3072,  # Replace with your model dimensions
            metric="cosine",  # Replace with your model metric
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

        pc_index = pc.Index(pinecone_index_name)

    pinecone_vector_store = PineconeVectorStore(pc_index)

    # load nodes from MD files
    # TODO: skip missing MD files + warning message
    with open("../../datasets.json", "r") as fp:
        datasets = [CDSDataset(**doc) for doc in json.load(fp)["cds-files"]]

    storage_context = StorageContext.from_defaults(
        vector_store=pinecone_vector_store, docstore=SimpleDocumentStore()
    )

    embed_model = OpenAIEmbedding(
        api_key=openai_api_key, model=OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE
    )

    await asyncio.gather(
        *(
            upload_dataset_to_vectorstore(
                input_dir="../cds/md",
                dataset=dataset,
                storage_context=storage_context,
                embed_model=embed_model,
            )
            # for dataset in datasets
            for dataset in datasets
        )
    )

    # for node in nodes:
    #     print(node.get_type())
    #     print(node.text)
    #     print(node.relationships)


if __name__ == "__main__":
    asyncio.run(main())
