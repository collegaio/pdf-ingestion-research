# from typing import List
# import dotenv
# from fsspec import AbstractFileSystem

# from llama_parse import LlamaParse

# import s3fs


# dotenv.load_dotenv("../.env")

# llama_cloud_api_key = os.environ["LLAMA_CLOUD_API_KEY"]
# openai_api_key = os.environ["OPENAI_API_KEY"]
# pinecone_api_key = os.environ["PINECONE_API_KEY"]

# s3_url = "https://seskderhisdikbcyrwcw.supabase.co/storage/v1/s3"
# # s3_region = "us-west-1"
# s3_access_key_id = os.environ["S3_ACCESS_KEY_ID"]
# s3_secret_access_key = os.environ["S3_SECRET_ACCESS_KEY"]
from urllib.parse import unquote_plus
import base64
import asyncio
import json
import os
import tempfile

from anthropic import AsyncAnthropicBedrock
import pymupdf
import s3fs

from dataset_tools.cds.models import CDSDataset


client = AsyncAnthropicBedrock()

datasets_bucket = os.getenv("DATASETS_BUCKET", "s3://collega-datasets-533267152364")


async def convert_markdown(input_file_path: str, output_file_path: str):
    with open(output_file_path, "w") as fp:
        doc = pymupdf.open(input_file_path)

        for page in doc:  # iterate through the pages
            pix = page.get_pixmap()  # render page to an image
            # pix.save(os.path.join(tempdir, "page-%i.png" % page.number))  # store image as a PNG
            encoded_string = base64.b64encode(pix.tobytes())
            # print(encoded_string)

            prompt = """
            Convert this image of a page from a PDF into markdown.
            Convert the tables to valid markdown tables.
            If there is an image or figure, replace it with an alternative text description.
            Return the formatted markdown in a block starting with "<MARKDOWN>" and ending with "</MARKDOWN>"
            """

            message = await client.messages.create(
                model="anthropic.claude-3-5-sonnet-20240620-v1:0",
                # model="anthropic.claude-3-haiku-20240307-v1:0",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": encoded_string.decode("utf-8"),
                                },
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )

            content = message.content

            if content != [] and content[0].type == "text":
                text = content[0].text
                print("before:", text)

                sub1 = "<MARKDOWN>"
                sub2 = "</MARKDOWN>"

                idx1 = 0
                idx2 = len(text)
                # print(text)
                try:
                    idx1 = text.index(sub1)
                except ValueError:
                    pass

                try:
                    idx2 = text.index(sub2)
                except ValueError:
                    pass

                # length of substring 1 is added to
                # get string from next character
                res = text[idx1 + len(sub1) + 1 : idx2]

                print("after:", res)
                fp.write(res)


# async def parse_and_save_document(input_dir: str, output_dir: str, dataset: CDSDataset):
#     print(f"loading documents for: {dataset.id}")
#     parser = LlamaParse(
#         result_type="markdown",
#         api_key=llama_cloud_api_key,
#         gpt4o_mode=True,
#         # gpt4o_api_key=openai_api_key,
#     )

#     # reader = SimpleDirectoryReader(
#     #     input_files=[os.path.join(input_dir, dataset.filename)],
#     #     # fs=fs,
#     #     file_extractor={".pdf": parser},
#     # )

#     # documents = await reader.aload_data()
#     documents = await parser.aload_data(os.path.join(input_dir, dataset.filename))
#     print("documents loaded:", len(documents))

#     if documents == []:
#         print("no source documents parsed for dataset:", dataset.id)
#         return

#     path = os.path.join(output_dir, f"{dataset.id}.md")
#     with open(path, "w") as fp:
#         for document in documents:
#             fp.write(document.text)

#     print(f"saved md for {dataset.id} to {path}")
#     # for node in nodes:
#     # fp.write(node.text)


async def main():
    # cds_files = s3fs.S3FileSystem(
    #     endpoint_url=s3_url, key=s3_access_key_id, secret=s3_secret_access_key
    # )

    # cds_files.ls("llm-training-data-bucket/cds-files")
    # TODO: download PDFs

    with open("../../datasets.json", "r") as fp:
        datasets = [CDSDataset(**doc) for doc in json.load(fp)["cds-files"]]

    # await asyncio.gather(
    #     *(
    #         parse_and_save_document(
    #             input_dir="../cds/pdf",
    #             output_dir="../cds/md",
    #             dataset=dataset,
    #         )
    #         for dataset in datasets
    #         # if dataset.id in set(["arizona-state"])
    #     )
    # )
    await asyncio.gather(
        *(
            convert_markdown(
                input_file_path=dataset.filename,
                output_file_path=os.path.join("../cds/md", f"{dataset.id}.md"),
            )
            for dataset in datasets
            # if dataset.id in set(["arizona-state"])
        )
    )


async def s3_transform_file(input_file: str, output_dir: str):
    fs = s3fs.S3FileSystem()

    with tempfile.TemporaryDirectory() as tempdir:
        fs.get(input_file, tempdir)

        input_path = os.path.join(tempdir, os.path.basename(input_file))
        output_path = os.path.join(
            tempdir, os.path.splitext(os.path.basename(input_file))[0] + ".md"
        )

        await convert_markdown(input_path, output_path)
        fs.put(output_path, os.path.join(output_dir, os.path.basename(output_path)))


# event: {
#     "Records": [
#         {
#             "eventVersion": "2.1",
#             "eventSource": "aws:s3",
#             "awsRegion": "us-east-1",
#             "eventTime": "2024-06-26T19:56:42.517Z",
#             "eventName": "ObjectCreated:Put",
#             "userIdentity": {"principalId": "A3L7Z8BNV2JKTI"},
#             "requestParameters": {"sourceIPAddress": "71.105.140.6"},
#             "responseElements": {
#                 "x-amz-request-id": "XYGWVT7ATZ964CB5",
#                 "x-amz-id-2": "s5xBkyGtl9esQzVV7V2dv2vnzPcfnShDdhQhpFM3jnuS8EBooICGjPNEtGFCoel5BB5SWKr99BCr50AJxFHOyXCDkBbnI7f2",
#             },
#             "s3": {
#                 "s3SchemaVersion": "1.0",
#                 "configurationId": "tf-s3-lambda-20240626194547870800000001",
#                 "bucket": {
#                     "name": "collega-cds-files-939879343571",
#                     "ownerIdentity": {"principalId": "A3L7Z8BNV2JKTI"},
#                     "arn": "arn:aws:s3:::collega-cds-files-939879343571",
#                 },
#                 "object": {
#                     "key": "Indiana+University-Bloomington+CDS_2023-2024.pdf",
#                     "size": 780615,
#                     "eTag": "52b15a8f18e14f6b6d79728f69b9c7fe",
#                     "sequencer": "00667C727A568D5324",
#                 },
#             },
#         }
#     ]
# }


def lambda_handler(event, context):
    # TODO: download from S3
    # TODO: upload to S3
    try:
        bucket = filename = event["Records"][0]["s3"]["bucket"]["name"]
        filename = event["Records"][0]["s3"]["object"]["key"]

        filepath = os.path.join("s3://", bucket, unquote_plus(filename))
        output_folder = os.path.join(datasets_bucket, os.path.dirname(filename))
        print(f"processing file: {filepath} -> {output_folder}")

        asyncio.run(s3_transform_file(filepath, output_folder))
    except Exception as e:
        print("Exception occured while processing PDF:", e)


if __name__ == "__main__":
    asyncio.run(main())
