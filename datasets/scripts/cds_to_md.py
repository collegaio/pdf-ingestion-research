import asyncio
import json
import os
from typing import List
import dotenv
from fsspec import AbstractFileSystem

from pinecone import Pinecone, ServerlessSpec
from llama_parse import LlamaParse

from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.core.schema import ObjectType, Document
from llama_index.core.schema import BaseNode, TextNode
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.readers.base import BasePydanticReader
from llama_index.embeddings.openai import OpenAIEmbedding
import s3fs

from dataset_tools.cds.models import CDSDataset

dotenv.load_dotenv("../.env")

llama_cloud_api_key = os.environ["LLAMA_CLOUD_API_KEY"]
openai_api_key = os.environ["OPENAI_API_KEY"]
pinecone_api_key = os.environ["PINECONE_API_KEY"]

s3_url = "https://seskderhisdikbcyrwcw.supabase.co/storage/v1/s3"
# s3_region = "us-west-1"
s3_access_key_id = os.environ["S3_ACCESS_KEY_ID"]
s3_secret_access_key = os.environ["S3_SECRET_ACCESS_KEY"]

pinecone_index_name = "cds-index-test"


async def load_cds_documents(
    input_dir: str,
    datasets: List[CDSDataset],
    # fs: AbstractFileSystem,
    parser: BasePydanticReader,
):
    reader = SimpleDirectoryReader(
        input_files=(os.path.join(input_dir, doc.filename) for doc in datasets),
        # fs=fs,
        file_extractor={".pdf": parser},
    )

    return await reader.aload_data()


def save_documents(
    output_dir: str, documents: List[Document], datasets: List[CDSDataset]
):
    datasets_by_filename = {doc.filename: doc for doc in datasets}

    for document in documents:
        dataset = datasets_by_filename[document.metadata["file_name"]]

        with open(os.path.join(output_dir, f"{dataset.id}.md"), "w") as fp:
            fp.write(document.text)


async def main():
    # cds_files = s3fs.S3FileSystem(
    #     endpoint_url=s3_url, key=s3_access_key_id, secret=s3_secret_access_key
    # )

    # cds_files.ls("llm-training-data-bucket/cds-files")
    # TODO: download files to PDF
    parser = LlamaParse(
        result_type="markdown",
        api_key=llama_cloud_api_key,
    )

    with open("../../datasets.json", "r") as fp:
        datasets = [CDSDataset(**doc) for doc in json.load(fp)["cds-files"]]

    documents = await load_cds_documents(
        # input_dir="llm-training-data-bucket/cds-files",
        input_dir="../cds/pdf",
        datasets=datasets[10:11],
        # fs=cds_files,
        parser=parser,
    )

    # print(documents)
    # TODO: clear MD files
    save_documents("../cds/md", documents, datasets)


if __name__ == "__main__":
    asyncio.run(main())
