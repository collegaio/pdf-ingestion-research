from enum import Enum
from typing import List, Optional

from llama_index.core.tools import FunctionTool
from pydantic import BaseModel
import requests

from chatbot.config import constants
from chatbot.config import env


class CollegeScorecardSchoolStates(str, Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"


class CollegeScorecardSchoolResponse(BaseModel):
    completion_rate: float
    latest_student_size: int
    name: str


def get_schools(
    states: Optional[List[CollegeScorecardSchoolStates]] = None,
    size_min: Optional[int] = None,
    size_max: Optional[int] = None,
):
    """
    Retrieves US colleges with options to filter by state or size

    Args:
        states (Optional[List[SchoolStates]]): List of US states to include colleges from
        size_min (Optional[int]): Specify minimum amount of students enrolled in college.
        size_max (Optional[int]): Specify maximum amount of students enrolled in college.

    Returns:
        List[SchoolResponse]: The list of US colleges filtered by the query.
    """
    params = {
        "api_key": env.COLLEGE_SCORECARD_API_KEY,
        "school.operating": 1,
        "latest.completion.completion_rate_4yr_150nt_pooled__range": ".80...99",
        "_fields": "school.name,latest.completion.completion_rate_4yr_150nt_pooled,latest.student.size,school.ownership",
        "_per_page": 25,
    }

    if states is not None:
        params["school.state"] = [state for state in states]

    if size_min is not None or size_max is not None:
        if size_min is None:
            size_min = 1_000

        if size_max is None:
            size_max = 50_000

        params["latest.student.size__range"] = f"{size_min}..{size_max}"

    # public or private?
    # "school.ownership": [1,2],

    response = requests.get(
        f"{constants.COLLEGE_SCORECARD_API_ENDPOINT}/schools.json", params=params
    )

    return [
        CollegeScorecardSchoolResponse(
            completion_rate=result[
                "latest.completion.completion_rate_4yr_150nt_pooled"
            ],
            latest_student_size=result["latest.student.size"],
            name=result["school.name"],
        )
        for result in response.json()["results"]
    ]


college_lookup_tool = FunctionTool.from_defaults(fn=get_schools)
