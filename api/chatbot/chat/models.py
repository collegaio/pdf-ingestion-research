from pydantic import BaseModel


class Datapoint(BaseModel):
    id: str
    description: str
