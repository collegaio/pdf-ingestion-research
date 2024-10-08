from typing import List

from pydantic import BaseModel, Field


class Datapoint(BaseModel):
    id: str
    description: str


class Dataset(BaseModel):
    id: str
    name: str
    description: str
    datapoints: List[Datapoint]
    datasets: List["Dataset"]


class StudentProfile(BaseModel):
    unweighted_gpa: float | None = Field(
        description="The student's unweighted GPA", default=None
    )
    geographic_preferences: List[str] | None = Field(
        description="The student's preferred geographic locations, such as 'The East Coast' or 'The South'",
        default=None,
    )
