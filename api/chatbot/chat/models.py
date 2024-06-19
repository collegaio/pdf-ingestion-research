from pydantic import BaseModel


class CDSDataset(BaseModel):
    id: str
    filename: str
    description: str
