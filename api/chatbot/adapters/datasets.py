import json
from re import T
from typing import Dict, List, Optional
import os

# import aiobotocore.session
import botocore.session
from pydantic import BaseModel, Field
import s3fs

from chatbot.config import env
from chatbot.chat.models import Datapoint, Dataset


class DatasetProperties(BaseModel):
    description: str
    datapoint_prefix: str


class DatasetConfig(BaseModel):
    properties: DatasetProperties
    datasets: Optional[Dict[str, "DatasetsConfig"]] = None


class DatasetsConfig(BaseModel):
    datasets: Dict[str, DatasetConfig]


def load_dataset(
    fs: s3fs.S3FileSystem, current_path: str, dataset: DatasetConfig
) -> Dataset:
    # if "datasets" in dataset:
    #     for sub_dataset in dataset["datasets"]:
    #         load_dataset(fs, os.path.join(current_path, sub_dataset), dataset["datasets"][sub_dataset])

    properties = dataset.properties
    datapoints = []

    for file in fs.glob(current_path + "/*.md"):
        datapoint_id = os.path.basename(os.path.splitext(file)[0])

        datapoint = Datapoint(
            id=datapoint_id,
            description=f"{properties.datapoint_prefix}{datapoint_id}",
        )

        datapoints.append(datapoint)

    nested_datasets = []

    if dataset.datasets is not None:
        for nested_dataset in dataset.datasets:
            nested_dataset = load_dataset(
                fs,
                os.path.join(current_path, nested_dataset),
                dataset.datasets[nested_dataset],
            )

            nested_datasets.append(nested_dataset)

    return Dataset(
        id=current_path,
        name=os.path.basename(current_path),
        description=dataset.properties.description,
        datapoints=datapoints,
        datasets=nested_datasets,
    )


def load_datasets(config: DatasetsConfig) -> List[Dataset]:
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
    datasets = []

    for key in config.datasets:
        dataset = load_dataset(
            fs,
            os.path.join(env.DATASETS_BUCKET, key),
            config.datasets[key],
        )

        datasets.append(dataset)

    return datasets
