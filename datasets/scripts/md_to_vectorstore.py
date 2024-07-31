import asyncio
import json
import os
import tempfile

# from typing import List
from typing import Optional
from urllib.parse import unquote_plus

# import dotenv

from pinecone import Pinecone

from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.core.ingestion.pipeline import DocstoreStrategy

# from llama_index.core import SimpleDirectoryReader

# from llama_index.core.schema import BaseNode
from llama_index.core.embeddings import BaseEmbedding

# from llama_index.core.llms import LLM
from llama_index.core.vector_stores.types import BasePydanticVectorStore
from llama_index.core.storage.docstore.keyval_docstore import KVDocumentStore

# from llama_index.core.node_parser import MarkdownNodeParser, MarkdownElementNodeParser
from llama_index.core.node_parser import MarkdownNodeParser

from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.storage.docstore.dynamodb import DynamoDBDocumentStore
from llama_index.embeddings.bedrock import BedrockEmbedding
import s3fs

from dataset_tools.cds.models import CDSDataset

# dotenv.load_dotenv("../.env")

pinecone_api_key = os.environ["PINECONE_API_KEY"]

index_name = "collega-datasets"

EMBED_MODEL: Optional[BaseEmbedding] = None
DOCSTORE: Optional[KVDocumentStore] = None
VECTORSTORE: Optional[BasePydanticVectorStore] = None


def setup():
    pc = Pinecone(api_key=pinecone_api_key)
    pc_index = pc.Index(index_name)

    global VECTORSTORE
    global DOCSTORE
    global EMBED_MODEL

    VECTORSTORE = PineconeVectorStore(pc_index)
    DOCSTORE = DynamoDBDocumentStore.from_table_name(table_name=index_name)
    # DOCSTORE = SimpleDocumentStore()
    EMBED_MODEL = BedrockEmbedding(model_name="cohere.embed-english-v3")


async def upload_dataset_to_vectorstore(
    input_file: str,
    dataset_group: Optional[str] = None,
):
    dataset_id = os.path.splitext(os.path.basename(input_file))[0]
    reader = SimpleDirectoryReader(
        input_files=[input_file],
    )

    documents = await reader.aload_data()

    for idx, document in enumerate(documents):
        # print("document:", document.doc_id)
        print("hash:", document.hash)
        # TODO: parser for XLSX format (it is just gibberish)
        document.doc_id = f"{dataset_id}-{idx}"
        document.metadata["dataset_id"] = dataset_id

        if dataset_group is not None:
            document.metadata["dataset_group"] = dataset_group

    pipeline = IngestionPipeline(
        transformations=[MarkdownNodeParser(), EMBED_MODEL],
        docstore=DOCSTORE,
        vector_store=VECTORSTORE,
        docstore_strategy=DocstoreStrategy.DUPLICATES_ONLY,
    )

    # await pipeline.arun(documents=documents)
    pipeline.run(documents=documents)
    # nodes = await pipeline.arun(documents=documents)
    # nodes = pipeline.run(documents=documents)

    # return VectorStoreIndex(
    #     nodes=nodes, storage_context=storage_context, embed_model=embed_model
    # )


async def main():
    setup()
    # print("existing indexes:", pc.list_indexes())

    # NOTE: to create index:
    # pc.create_index(
    #     name=pinecone_index_name,
    #     dimension=3072,  # Replace with your model dimensions
    #     metric="cosine",  # Replace with your model metric
    #     spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    # )

    # load nodes from MD files
    # TODO: skip missing MD files + warning message
    with open("../../datasets.json", "r") as fp:
        datasets = [CDSDataset(**doc) for doc in json.load(fp)["cds-files"]]

    await asyncio.gather(
        *(
            upload_dataset_to_vectorstore(
                input_file=os.path.join("../cds/md", f"{dataset.id}.md"),
                dataset_group="cds-files",
            )
            # for dataset in datasets
            for dataset in datasets
        )
    )

    # for node in nodes:
    #     print(node.get_type())
    #     print(node.text)
    #     print(node.relationships)


async def s3_transform_file(input_file: str, dataset_group: str):
    fs = s3fs.S3FileSystem()

    with tempfile.TemporaryDirectory() as tempdir:
        fs.get(input_file, tempdir)

        await upload_dataset_to_vectorstore(
            input_file=os.path.join(tempdir, os.path.basename(input_file)),
            dataset_group=dataset_group,
            # docstore=DOCSTORE,
            # vector_store=VECTOR_STORE,
        )


def lambda_handler(event, context):
    setup()

    try:
        bucket = filename = event["Records"][0]["s3"]["bucket"]["name"]
        filename = event["Records"][0]["s3"]["object"]["key"]

        filepath = os.path.join("s3://", bucket, unquote_plus(filename))
        print(f"processing file: {filepath}")

        asyncio.run(
            s3_transform_file(
                input_file=filepath,
                dataset_group=os.path.basename(unquote_plus(filename)),
            )
        )
    except Exception as e:
        print("Exception occured while processing PDF:", e)


if __name__ == "__main__":
    asyncio.run(main())
