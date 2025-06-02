"""Tests for the cleaning.py module."""

import pandas as pd
from life_expectancy.cleaning import clean_data, main
from life_expectancy.region_enum import Region
from . import OUTPUT_DIR


def test_clean_data_with_fixture(eu_life_expectancy_raw, eu_life_expectancy_expected):
    """Compares the output of clean_data with the expected result."""
    result_df = clean_data(eu_life_expectancy_raw, region=Region.PT)

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        eu_life_expectancy_expected.reset_index(drop=True)
    )


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    main(Region.PT)
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual.reset_index(drop=True),
        pt_life_expectancy_expected.reset_index(drop=True)
    )
