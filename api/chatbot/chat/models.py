from typing import Dict, List, Optional
from pydantic import BaseModel


class Datapoint(BaseModel):
    id: str
    description: str


class Dataset(BaseModel):
    id: str
    name: str
    description: str
    datapoints: List[Datapoint]
    datasets: List["Dataset"]
