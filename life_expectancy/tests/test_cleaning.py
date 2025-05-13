"""Tests for the cleaning.py module."""

import pandas as pd

from life_expectancy.cleaning import clean_data

def test_clean_data_with_fixture(
    eu_life_expectancy_raw_fixture, eu_life_expectancy_expected_fixture
):
    """Compares the output of clean_data with the expected result."""
    result_df = clean_data(eu_life_expectancy_raw_fixture, region="PT")
    result_df = result_df[eu_life_expectancy_expected_fixture.columns]

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        eu_life_expectancy_expected_fixture.reset_index(drop=True)
    )
