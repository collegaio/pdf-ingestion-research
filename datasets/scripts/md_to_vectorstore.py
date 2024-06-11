import asyncio
import json
import os
from typing import List
import dotenv

from pinecone import Pinecone, ServerlessSpec

from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.core.schema import BaseNode
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

from dataset_tools.cds.models import CDSDataset

dotenv.load_dotenv("../.env")


openai_api_key = os.environ["OPENAI_API_KEY"]
pinecone_api_key = os.environ["PINECONE_API_KEY"]

pinecone_index_name = "cds-index-test"


async def load_markdown_files(input_dir: str, datasets: List[CDSDataset]):
    datasets_by_filename = {f"{doc.id}.md": doc for doc in datasets}

    reader = SimpleDirectoryReader(
        input_files=(os.path.join(input_dir, f"{doc.id}.md") for doc in datasets),
    )

    documents = await reader.aload_data()

    for document in documents:
        dataset = datasets_by_filename[document.metadata["file_name"]]

        # TODO: parser for XLSX format (it is just gibberish)
        document.doc_id = dataset.id
        document.metadata["dataset_id"] = dataset.id
        document.metadata["dataset_group"] = "cds-data"

    pipeline = IngestionPipeline(transformations=[MarkdownNodeParser()])

    return await pipeline.arun(documents=documents)


def add_nodes_to_index(
    nodes: List[BaseNode],
    vector_store: SimpleVectorStore,
    embed_model: BaseEmbedding,
):
    # construct vector store and customize storage context
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store, docstore=SimpleDocumentStore()
    )

    # batch insert nodes so we don't hit the embed API too many times
    # Settings.chunk_size = 32
    # Settings.chunk_overlap = 50

    return VectorStoreIndex(
        nodes=nodes, storage_context=storage_context, embed_model=embed_model
    )


async def main():
    embed_model = OpenAIEmbedding(api_key=openai_api_key)

    pc = Pinecone(api_key=pinecone_api_key)
    print("existing indexes:", pc.list_indexes())

    if pinecone_index_name in (index["name"] for index in pc.list_indexes()):
        pc_index = pc.Index(pinecone_index_name)

        # if pc_index.describe_index_stats()['total_vector_count'] > 0:
        #     pc_index.delete(ids=[vector_id for vector_id in pc_index.list()], namespace="")
    else:
        pc.create_index(
            name=pinecone_index_name,
            dimension=1536,  # Replace with your model dimensions
            metric="cosine",  # Replace with your model metric
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

        pc_index = pc.Index(pinecone_index_name)

    pinecone_vector_store = PineconeVectorStore(pc_index)

    # load nodes from MD files
    # TODO: skip missing MD files + warning message
    with open("../../datasets.json", "r") as fp:
        datasets = [CDSDataset(**doc) for doc in json.load(fp)["cds-files"]][11:12]

    nodes = await load_markdown_files("../cds/md", datasets)

    add_nodes_to_index(
        nodes=nodes, vector_store=pinecone_vector_store, embed_model=embed_model
    )


if __name__ == "__main__":
    asyncio.run(main())
