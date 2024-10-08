import polars as pl

from chatbot.pipelines import recommendations


def test_filter_colleges_by_gpa_clean_data():
    df = pl.DataFrame(
        {
            "percent_who_had_gpa_of_4": [70, 50],
            "percent_who_had_gpa_between_3_75_and_3_99": [25, 30],
            "percent_who_had_gpa_between_3_50_and_3_74": [4, 10],
            "percent_who_had_gpa_between_3_25_and_3_49": [1, 5],
            "percent_who_had_gpa_between_3_00_and_3_24": [0, 2],
            "percent_who_had_gpa_between_2_50_and_2_99": [0, 1],
            "percent_who_had_gpa_between_2_0_and_2_49": [0, 1],
            "percent_who_had_gpa_between_1_0_and_1_99": [0, 1],
            "percent_who_had_gpa_below_1": [0, 0],
        }
    )

    colleges = recommendations.filter_colleges_by_gpa(3.49, df)
    # should return the second college
    assert len(colleges) == 1


def test_filter_colleges_by_gpa_empty_data():
    df = pl.DataFrame(
        {
            "percent_who_had_gpa_of_4": [70, None],
            "percent_who_had_gpa_between_3_75_and_3_99": [25, None],
            "percent_who_had_gpa_between_3_50_and_3_74": [4, None],
            "percent_who_had_gpa_between_3_25_and_3_49": [1, None],
            "percent_who_had_gpa_between_3_00_and_3_24": [0, None],
            "percent_who_had_gpa_between_2_50_and_2_99": [0, None],
            "percent_who_had_gpa_between_2_0_and_2_49": [0, None],
            "percent_who_had_gpa_between_1_0_and_1_99": [0, None],
            "percent_who_had_gpa_below_1": [0, None],
        }
    )

    colleges = recommendations.filter_colleges_by_gpa(3.49, df)
    # should return the second college
    assert len(colleges) == 1


def test_filter_colleges_by_gpa_incomplete_data():
    df = pl.DataFrame(
        {
            "percent_who_had_gpa_of_4": [70, 50],
            "percent_who_had_gpa_between_3_75_and_3_99": [25, None],
            "percent_who_had_gpa_between_3_50_and_3_74": [4, None],
            "percent_who_had_gpa_between_3_25_and_3_49": [1, None],
            "percent_who_had_gpa_between_3_00_and_3_24": [0, 1],
            "percent_who_had_gpa_between_2_50_and_2_99": [0, 1],
            "percent_who_had_gpa_between_2_0_and_2_49": [0, 1],
            "percent_who_had_gpa_between_1_0_and_1_99": [0, 1],
            "percent_who_had_gpa_below_1": [0, 1],
        }
    )

    colleges = recommendations.filter_colleges_by_gpa(3.49, df)
    # should return no colleges
    assert len(colleges) == 0
