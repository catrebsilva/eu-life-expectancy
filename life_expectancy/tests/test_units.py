"""Unit tests for the cleaning module functions."""

from unittest.mock import patch
import pandas as pd

from life_expectancy.cleaning import load_data, clean_data, save_data

def test_load_data_returns_dataframe():
    """Check that load_data returns a non-empty DataFrame."""
    loaded_data = load_data()
    assert isinstance(loaded_data, pd.DataFrame)
    assert not loaded_data.empty

def test_clean_data_filters_and_transforms():
    """Check that clean_data filters for PT and transforms the data correctly."""
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
    """Check that save_data calls to_csv with the correct file name (mocked)."""
    sample_data = pd.DataFrame({"col1": [1], "col2": [2]})

    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        save_data(sample_data, region="PT")

        assert mock_to_csv.call_count == 1
        args, _ = mock_to_csv.call_args
        assert str(args[0]).endswith("pt_life_expectancy.csv")
