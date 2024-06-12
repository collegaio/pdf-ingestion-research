import asyncio
import json
import os
from typing import List
import dotenv
from fsspec import AbstractFileSystem

from llama_parse import LlamaParse

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


async def parse_and_save_document(input_dir: str, output_dir: str, dataset: CDSDataset):
    print(f"loading documents for: {dataset.id}")
    parser = LlamaParse(
        result_type="markdown",
        api_key=llama_cloud_api_key,
        gpt4o_mode=True,
        # gpt4o_api_key=openai_api_key,
    )

    # reader = SimpleDirectoryReader(
    #     input_files=[os.path.join(input_dir, dataset.filename)],
    #     # fs=fs,
    #     file_extractor={".pdf": parser},
    # )

    # documents = await reader.aload_data()
    documents = await parser.aload_data(os.path.join(input_dir, dataset.filename))
    print("documents loaded:", len(documents))

    if documents == []:
        print("no source documents parsed for dataset:", dataset.id)
        return

    path = os.path.join(output_dir, f"{dataset.id}.md")
    with open(path, "w") as fp:
        for document in documents:
            fp.write(document.text)

    print(f"saved md for {dataset.id} to {path}")
    # for node in nodes:
    # fp.write(node.text)


async def main():
    # cds_files = s3fs.S3FileSystem(
    #     endpoint_url=s3_url, key=s3_access_key_id, secret=s3_secret_access_key
    # )

    # cds_files.ls("llm-training-data-bucket/cds-files")
    # TODO: download PDFs

    with open("../../datasets.json", "r") as fp:
        datasets = [CDSDataset(**doc) for doc in json.load(fp)["cds-files"]]

    await asyncio.gather(
        *(
            parse_and_save_document(
                input_dir="../cds/pdf",
                output_dir="../cds/md",
                dataset=dataset,
            )
            for dataset in datasets
            # if dataset.id in set(["arizona-state"])
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
