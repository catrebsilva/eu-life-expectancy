"""Tests for the cleaning.py module"""

import pandas as pd
from life_expectancy.cleaning import load_data, clean_data, save_data
from unittest.mock import patch

def test_clean_data_with_fixture(eu_life_expectancy_raw_fixture, eu_life_expectancy_expected_fixture):
    """Compares the output of the clean_data function with the expected result."""
    result_df = clean_data(eu_life_expectancy_raw_fixture, region="PT")
    result_df = result_df[eu_life_expectancy_expected_fixture.columns]

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        eu_life_expectancy_expected_fixture.reset_index(drop=True)
    )

def test_load_data_returns_dataframe():
    """Checks that load_data returns a non-empty DataFrame."""
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_clean_data_filters_only_selected_region():
    """Check that clean_data filters and cleans correctly for the PT region."""
    sample_data = pd.DataFrame({
        "unit,sex,age,geo\\time": ["YR,LIFE,0,PT", "YR,LIFE,0,FR", "YR,LIFE,0,PT"],
        "2019": ["82.5", "80.1", "83.2"],
        "2020": ["82.0", "79.9", ": "]
    })

    result = clean_data(sample_data, region="PT")

    assert not result.empty
    assert all(result["region"] == "PT")
    assert set(result.columns) == {"unit", "sex", "age", "region", "year", "value"}

def test_save_data_calls_to_csv_with_correct_filename():
    """Check that save_data calls to_csv with the correct name (mock)."""
    df = pd.DataFrame({"col1": [1], "col2": [2]})

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        save_data(df, region="PT")

        assert mock_to_csv.call_count == 1
        args, _ = mock_to_csv.call_args
        assert str(args[0]).endswith("pt_life_expectancy.csv")
