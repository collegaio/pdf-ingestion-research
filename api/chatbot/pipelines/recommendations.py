from typing import List

from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
import polars as pl

from chatbot.config.clients import cohere_langchain_llm
from chatbot.chat.models import StudentProfile


def filter_colleges_by_gpa(student_gpa: float, colleges: pl.DataFrame):
    """
    Recommend schools where the total of the GPA brackets is at least 10%.
    If the student's GPA is not in the data, use the default percentages.

    Args:
        student_gpa (float): The student's GPA.
        colleges (pl.DataFrame): A DataFrame of colleges with their corresponding GPA brackets.

    Returns:
        pl.DataFrame: A DataFrame of colleges that are recommended for the student.
    """

    # Define GPA brackets and their corresponding column names
    # threshold, description, default
    gpa_brackets = [
        (4.0, "percent_who_had_gpa_of_4", 50),
        (3.75, "percent_who_had_gpa_between_3_75_and_3_99", 20),
        (3.5, "percent_who_had_gpa_between_3_50_and_3_74", 15),
        (3.25, "percent_who_had_gpa_between_3_25_and_3_49", 10),
        (3.0, "percent_who_had_gpa_between_3_00_and_3_24", 5),
        (2.5, "percent_who_had_gpa_between_2_50_and_2_99", 2),
        (2.0, "percent_who_had_gpa_between_2_0_and_2_49", 1),
        (1.0, "percent_who_had_gpa_between_1_0_and_1_99", 0.5),
        (0.0, "percent_who_had_gpa_below_1", 0.5),
    ]

    # Determine student's GPA bracket
    student_bracket_index = next(
        (
            i
            for i, (threshold, _, _) in enumerate(gpa_brackets)
            if student_gpa >= threshold
        ),
        len(gpa_brackets) - 1,
    )

    # Compute the sum of all columns from the student's bracket onwards
    bracket_cols = [col for _, col, _ in gpa_brackets[student_bracket_index:]]
    default_sum = sum(default for _, _, default in gpa_brackets[student_bracket_index:])

    colleges = colleges.with_columns(
        pl.when(pl.sum_horizontal(bracket_cols) == 0)
        .then(pl.lit(default_sum))
        .otherwise(pl.sum_horizontal(bracket_cols))
        .alias("gpa_bracket_sum")
    )

    # Filter colleges where the sum is at least 10%
    filtered_colleges = colleges.filter(pl.col("gpa_bracket_sum") >= 10)

    return filtered_colleges


def filter_colleges_by_geographic_preferences(
    preferences: List[str], colleges: pl.DataFrame
):
    """
    Filter colleges by geographic preferences.
    If no exact matches are found, return the closest matches.

    Args:
        preferences (List[str]): The student's geographic preferences.
        colleges (pl.DataFrame): A DataFrame of colleges with their corresponding dataset IDs.

    Returns:
        pl.DataFrame: A DataFrame of colleges that are recommended for the student.
    """
    if preferences == []:
        return colleges

    # Extract dataset_id from colleges
    dataset_ids = colleges["dataset_id"].unique().to_list()

    # Prepare the prompt template
    prompt_template = PromptTemplate(
        input_variables=["preferences", "dataset_ids"],
        template="""
        Given the following geographic preferences: {preferences}
        And the following list of college dataset IDs: {dataset_ids}
        
        Please return a comma-separated list of dataset IDs that match the geographic preferences.
        If no exact matches are found, return the closest matches.
        Only return the dataset IDs, nothing else.
        """,
    )

    # Prepare the output parser
    output_parser = CommaSeparatedListOutputParser()

    # Combine the prompt template and output parser
    chain = prompt_template | cohere_langchain_llm | output_parser

    # Run the chain
    matching_dataset_ids = chain.invoke(
        {"preferences": ", ".join(preferences), "dataset_ids": ", ".join(dataset_ids)}
    )

    # Filter colleges by the matching dataset IDs
    filtered_colleges = colleges.filter(
        pl.col("dataset_id").is_in(matching_dataset_ids)
    )

    return filtered_colleges


def recommend_colleges(student_profile: StudentProfile):
    # TODO: filter colleges based on GPA if not None
    # TODO: filter out schools based on geographic preferences if not None and not empty
    return
