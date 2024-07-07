import json
from re import T
from typing import Dict, List
import os

# import aiobotocore.session
import botocore.session
from pydantic import BaseModel, Field
import s3fs

from chatbot.config import env
from chatbot.chat.models import Datapoint


class DatasetProperties(BaseModel):
    description: str


class DatasetConfig(BaseModel):
    properties: DatasetProperties


class DatasetsConfig(BaseModel):
    datasets: Dict[str, DatasetConfig]


def load_dataset(
    fs: s3fs.S3FileSystem, current_path: str, dataset: DatasetConfig
) -> List[Datapoint]:
    # if "datasets" in dataset:
    #     for sub_dataset in dataset["datasets"]:
    #         load_dataset(fs, os.path.join(current_path, sub_dataset), dataset["datasets"][sub_dataset])

    properties = dataset.properties
    datapoints = []

    for file in fs.glob(current_path + "/*.md"):
        datapoint_id = os.path.basename(os.path.splitext(file)[0])

        datapoint = Datapoint(
            id=datapoint_id,
            description=f"{properties.description} for {datapoint_id}",
        )

        datapoints.append(datapoint)

    return datapoints


def load_datasets(config: DatasetsConfig) -> List[Datapoint]:
    # session = botocore.session.get_session()

    # client = session.create_client(
    #     "sts",
    #     # region_name="us-east-1",
    #     # aws_access_key_id=env.S3_ACCESS_KEY_ID,
    #     # aws_secret_access_key=env.S3_SECRET_ACCESS_KEY,
    # )

    # credentials = client.get_session_token()["Credentials"]
    # print(env.AWS_ACCESS_KEY_ID)
    # print(env.AWS_SECRET_ACCESS_KEY)
    fs = s3fs.S3FileSystem(
        key=env.AWS_ACCESS_KEY_ID,
        secret=env.AWS_SECRET_ACCESS_KEY,
    )
    # fs = s3fs.S3FileSystem(token=credentials["SessionToken"])
    all_datasets = []

    for key in config.datasets:
        # TODO: get bucket from config
        # TODO: set s3 creds in config
        datasets = load_dataset(
            fs,
            os.path.join(env.DATASETS_BUCKET, key),
            config.datasets[key],
        )
        all_datasets.extend(datasets)

    return all_datasets
