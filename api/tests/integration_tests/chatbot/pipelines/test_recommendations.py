import polars as pl

from chatbot.pipelines.recommendations import filter_colleges_by_geographic_preferences


def test_filter_colleges_by_geographic_preferences():
    colleges = pl.DataFrame(
        {
            "dataset_id": ["Stanford", "Berkeley", "MIT", "Harvard", "Yale"],
        }
    )

    filtered_colleges = filter_colleges_by_geographic_preferences(
        ["California"], colleges
    )

    assert len(filtered_colleges) == 2

    filtered_names = filtered_colleges["dataset_id"].to_list()
    assert "Stanford" in filtered_names
    assert "Berkeley" in filtered_names
