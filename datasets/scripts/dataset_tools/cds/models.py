from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class CDSDataset(BaseModel):
    """Represents a CDS PDF document for a school"""

    id: str
    filename: str
    description: str


class AcceptedApplicantInfo(BaseModel):
    """Represents male and female applicant information"""

    first_year_applied_male: int = Field(
        description="Total first year full time male applicants"
    )
    first_year_applied_female: int = Field(
        description="Total first year full time female applicants"
    )
    first_year_accepted_male: int = Field(
        description="Total first year full time male applicants who were accepted"
    )
    first_year_accepted_female: int = Field(
        description="Total first year full time female applicants who were accepted"
    )
    first_year_enrolled_male: int = Field(
        description="Total first year full time male applicants who enrolled"
    )
    first_year_enrolled_female: int = Field(
        description="Total first year full time female applicants who enrolled"
    )


class ResidencyInfo(BaseModel):
    """residency breakdowns for total applicants, admits, and enrolled students"""

    first_year_applied_in_state: int = Field(
        description="Total number of first year applicants who were in state"
    )
    first_year_applied_out_of_state: int = Field(
        description="Total number of first year applicants who were out of state"
    )
    first_year_applied_international: int = Field(
        description="Total number of first year applicants who were international"
    )
    first_year_accepted_in_state: int = Field(
        description="Total number of first year applicants that were accepted who were in state"
    )
    first_year_accepted_out_of_state: int = Field(
        description="Total number of first year applicants that were accepted who were out of state"
    )
    first_year_accepted_international: int = Field(
        description="Total number of first year applicants that were accepted who were international"
    )
    first_year_enrolled_in_state: int = Field(
        description="Total number of first year students that enrolled who were in state"
    )
    first_year_enrolled_out_of_state: int = Field(
        description="Total number of first year students that enrolled who were out of state"
    )
    first_year_enrolled_international: int = Field(
        description="Total number of first year students that enrolled who were international"
    )


class WaitListInfo(BaseModel):
    """Breakdown of waitlist information for first time first year students"""

    wait_list_size: int = Field(
        description="Total size of admissions wait list", default=0
    )
    wait_list_admitted: int = Field(
        description="Number of students on wait list who were admitted", default=0
    )
    wait_list_ranked: bool = Field(
        description="Whether or not the wait list is ranked", default=0
    )


class AdmissionsRequirementsInfo(BaseModel):
    """Breakdown of class unit requirements for admitted students"""

    # high_school_diploma_ged_required: bool = Field(
    #     description="Whether or not high school diploma or GED is required for admission"
    # )
    # ged_acceped: bool = Field(
    #     description="Whether or not a GED is accepted for admission"
    # )
    english_credits_required: int = Field(
        description="Number of english credits required for admitted applicants",
        default=0,
    )
    english_credits_recommended: int = Field(
        description="Number of english credits recommended for admitted applicants",
        default=4,
    )
    math_credits_required: int = Field(
        description="Number of math credits required for admitted applicants",
        default=0,
    )
    math_credits_recommended: int = Field(
        description="Number of math credits recommended for admitted applicants",
        default=4,
    )
    science_credits_required: int = Field(
        description="Number of science credits required for admitted applicants",
        default=0,
    )
    science_credits_recommended: int = Field(
        description="Number of science credits recommended for admitted applicants",
        default=3,
    )
    social_studies_credits_required: int = Field(
        description="Number of social studies credits required for admitted applicants",
        default=0,
    )
    social_studies_credits_recommended: int = Field(
        description="Number of social studies credits recommended for admitted applicants",
        default=0,
    )
    history_credits_required: int = Field(
        description="Number of history credits recommended for admitted applicants",
        default=0,
    )
    history_credits_recommended: int = Field(
        description="Number of history credits recommended for admitted applicants",
        default=2,
    )
    elective_credits_required: int = Field(
        description="Number of elective credits required for admitted applicants",
        default=0,
    )
    elective_credits_recommended: int = Field(
        description="Number of elective credits recommended for admitted applicants",
        default=0,
    )
    performing_arts_credits_required: int = Field(
        description="Number of performing arts credits required for admitted applicants",
        default=0,
    )
    performing_arts_credits_recommended: int = Field(
        description="Number of performing arts credits recommended for admitted applicants",
        default=0,
    )
    computer_science_credits_required: int = Field(
        description="Number of computer science credits required for admitted applicants",
        default=0,
    )
    computer_science_credits_recommended: int = Field(
        description="Number of computer science credits recommended for admitted applicants",
        default=0,
    )
    performing_arts_credits_required: int = Field(
        description="Number of performing arts credits required for admitted applicants",
        default=0,
    )
    performing_arts_credits_recommended: int = Field(
        description="Number of performing arts credits recommended for admitted applicants",
        default=0,
    )
    foreign_language_credits_required: int = Field(
        description="Number of foreign language credits required for admitted applicants",
        default=0,
    )
    foreign_language_credits_recommended: int = Field(
        description="Number of foreign language credits recommended for admitted applicants",
        default=2,
    )


class AdmissionFactorWeightClass(str, Enum):
    very_important = "very important"
    important = "important"
    considered = "considered"
    not_considered = "not considered"


class AdmissionsFactorWeights(BaseModel):
    """Information about how heavily weighted certain factors are for admission to this institution"""

    class_rank: AdmissionFactorWeightClass = Field(
        description="Importance weighted on class rank"
    )
    gpa: AdmissionFactorWeightClass = Field(description="Importance weighted on gpa")
    standardized_test_score: AdmissionFactorWeightClass = Field(
        description="Importance weighted on standardized test scores"
    )
    essay: AdmissionFactorWeightClass = Field(
        description="Importance weighted on quality of essay"
    )
    interview: AdmissionFactorWeightClass = Field(
        description="Importance weighted on quality of essay"
    )
    extracurriculars: AdmissionFactorWeightClass = Field(
        description="Importance weighted on extracurriculars, volunteer, or work experience"
    )
    first_gen: AdmissionFactorWeightClass = Field(
        description="Importance weighted on being a first generation student"
    )
    alumni: AdmissionFactorWeightClass = Field(
        description="Importance weighted on if the student's parents are alumni"
    )
    residence: AdmissionFactorWeightClass = Field(
        description="Importance weighted on if the student lives out of state"
    )
    religion: AdmissionFactorWeightClass = Field(
        description="Importance weighted on what the student's religion is"
    )


class StandardizedTestScoreInfo(BaseModel):
    """Breakdown of standardized test scores for admitted applicants"""

    sat_act_required: bool = Field(
        description="Are applicants required to submit their SAT or ACT score?"
    )
    sat_accepted: bool = Field(
        description="Is the SAT accepted for admission to this institution?"
    )
    act_accepted: bool = Field(
        description="Is the ACT accepted for admission to this institution?"
    )
    sat_composite_25_percent: int = Field(
        description="25th percentile composite SAT score of admitted applicants"
    )
    sat_composite_50_percent: int = Field(
        description="50th percentile composite SAT score of admitted applicants"
    )
    sat_composite_75_percent: int = Field(
        description="75th percentile composite SAT score of admitted applicants"
    )
    sat_math_25_percent: int = Field(
        description="25th percentile composite SAT math score of admitted applicants"
    )
    sat_math_50_percent: int = Field(
        description="50th percentile composite SAT math score of admitted applicants"
    )
    sat_math_75_percent: int = Field(
        description="75th percentile composite SAT math score of admitted applicants"
    )
    sat_reading_25_percent: int = Field(
        description="25th percentile composite SAT reading score of admitted applicants"
    )
    sat_reading_50_percent: int = Field(
        description="50th percentile composite SAT reading score of admitted applicants"
    )
    sat_reading_75_percent: int = Field(
        description="75th percentile composite SAT reading score of admitted applicants"
    )
    act_composite_25_percent: int = Field(
        description="25th percentile composite ACT score of admitted applicants"
    )
    act_composite_50_percent: int = Field(
        description="50th percentile composite ACT score of admitted applicants"
    )
    act_composite_75_percent: int = Field(
        description="75th percentile composite ACT score of admitted applicants"
    )
    act_math_25_percent: int = Field(
        description="25th percentile composite ACT math score of admitted applicants"
    )
    act_math_50_percent: int = Field(
        description="50th percentile composite ACT math score of admitted applicants"
    )
    act_math_75_percent: int = Field(
        description="75th percentile composite ACT math score of admitted applicants"
    )
    act_english_25_percent: int = Field(
        description="25th percentile composite ACT english score of admitted applicants"
    )
    act_english_50_percent: int = Field(
        description="50th percentile composite ACT english score of admitted applicants"
    )
    act_english_75_percent: int = Field(
        description="75th percentile composite ACT english score of admitted applicants"
    )
    act_writing_25_percent: int = Field(
        description="25th percentile composite ACT writing score of admitted applicants"
    )
    act_writing_50_percent: int = Field(
        description="50th percentile composite ACT writing score of admitted applicants"
    )
    act_writing_75_percent: int = Field(
        description="75th percentile composite ACT writing score of admitted applicants"
    )
    act_science_25_percent: int = Field(
        description="25th percentile composite ACT science score of admitted applicants"
    )
    act_science_50_percent: int = Field(
        description="50th percentile composite ACT science score of admitted applicants"
    )
    act_science_75_percent: int = Field(
        description="75th percentile composite ACT science score of admitted applicants"
    )
    act_reading_25_percent: int = Field(
        description="25th percentile composite ACT reading score of admitted applicants"
    )
    act_reading_50_percent: int = Field(
        description="50th percentile composite ACT reading score of admitted applicants"
    )
    act_reading_75_percent: int = Field(
        description="75th percentile composite ACT reading score of admitted applicants"
    )


class ClassRankInfo(BaseModel):
    """Breakdown of class rank reported by students who were accepted at this institution"""

    top_tenth_percent: float = Field(
        description="Percent of applicants who were in the top tenth of their graduating class"
    )
    top_quarter_percent: float = Field(
        description="Percent of applicants who were in the top quarter of their graduating class"
    )
    top_half_percent: float = Field(
        description="Percent of applicants who were in the top half of their graduating class"
    )
    bottom_half_percent: float = Field(
        description="Percent of applicants who were in the bottom half of their graduating class"
    )
    bottom_quarter_percent: float = Field(
        description="Percent of applicants who were in the bottom quarter of their graduating class"
    )


class GPAInfo(BaseModel):
    """Breakdown of GPA reported by students who were accepted at this institution"""

    average_gpa: float = Field(description="Average GPA of degree seekers")


class ApplicationFees(BaseModel):
    """Breakdown of application fees for this institution"""

    application_fee: float = Field(description="Application fee cost")
    application_fee_waivable: bool = Field(
        description="Can this institution waive the application fee?"
    )


# class ApplicationDueDates(BaseModel):
#     """Breakdown of closing dates for applying to this school"""

#     application_closing_date: Optional[str] = Field(
#         description="Application due date for fall semester"
#     )
#     application_priority_date: Optional[str] = Field(
#         description="Priority date to submit application by"
#     )
#     early_action: bool = Field(description="Does this institution offer early action?")
#     early_action_date: Optional[str] = Field(
#         description="Date to submit application by for early action if offered"
#     )
#     early_decision: bool = Field(
#         description="Does this institution offer early decision?"
#     )
#     early_decision_date: Optional[str] = Field(
#         description="Date to submit application by for early decision if offered"
#     )


# in state tutition
# reciprocity tuition
# religious affiliation tuition
# states with reciprocity
# out of state tuition
# campus housing fees
# campus food fees
# books and supplies fees

# percent of first time freshmen awarded financial aid
# average aid package total
# average scholarship total
# average self help award total
# average need based loan award total

# aid types
# aid deadlines


class InstitutionCDSInfo(BaseModel):
    accepted_applicant_info: AcceptedApplicantInfo = Field(
        description="breakdown of male and female applicants"
    )
    residency_info: ResidencyInfo = Field(
        description="breakdown of where applicants were located"
    )
    # waitlist_info: WaitListInfo = Field(
    #     description="Information about the admissions waitlist"
    # )
    admissions_requirements_info: AdmissionsRequirementsInfo = Field(
        description="Class credit requirements applicants must meet to be elligible for admission"
    )
    # open_admissions_policy: OpenAdmissionsPolicy = Field(
    #     description="Information about this institutions open admissions policy"
    # )
    admissions_factor_weights: AdmissionsFactorWeights = Field(
        description="Information about how heavily weighted application factors are for applicants to this school"
    )
    standardized_test_score_info: StandardizedTestScoreInfo = Field(
        "Breakdown of standardized test scores for admitted students at this institution"
    )
    class_rank_info: ClassRankInfo = Field(
        description="Information about class rank of students at this institution"
    )
    gpa_info: GPAInfo = Field(
        description="Breakdown of GPA scores submitted by applicants who were accepted at this school"
    )
    # fees: ApplicationFees = Field(
    #     description="Breakdown of application fees for this school"
    # )
    # application_due_dates: ApplicationDueDates = Field(
    #     description="Due dates for application to this school"
    # )
