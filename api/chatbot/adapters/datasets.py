import json
from typing import List
from pydantic import BaseModel, Field

from chatbot.chat.models import CDSDataset


class DatasetsFile(BaseModel):
    cds_files: List[CDSDataset] = Field(alias="cds-files")


def load_datasets_file(path: str):
    with open(path, "r") as fp:
        return DatasetsFile(**json.load(fp))
