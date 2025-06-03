"""Tests for the cleaning.py module."""

import pandas as pd
import numpy as np
from life_expectancy.cleaning import clean_data, load_data
from life_expectancy.region_enum import Region
from life_expectancy.data_loader.tsv_loader import TSVLoader  # pylint: disable=unused-import
from life_expectancy.data_loader.json_loader import JSONLoader
from . import FIXTURES_DIR  # pylint: disable=unused-import

# def test_clean_data_tsv_loader(pt_life_expectancy_expected_tsv, eu_life_expectancy_tsv_path):
#     """Test full pipeline with TSVLoader."""
#     loader = TSVLoader()
#     raw_df = load_data(eu_life_expectancy_tsv_path, loader)
#     cleaned_df = clean_data(raw_df, region=Region.PT)
#
#     pd.testing.assert_frame_equal(
#         cleaned_df.fillna(np.nan).reset_index(drop=True),
#         pt_life_expectancy_expected_json.fillna(np.nan).reset_index(drop=True)
#     )

def test_clean_data_json_loader(
    pt_life_expectancy_expected_json, eurostat_life_expectancy_json_path
):
    """Test full pipeline with JSONLoader."""
    loader = JSONLoader()
    raw_df = load_data(eurostat_life_expectancy_json_path, loader)
    cleaned_df = clean_data(raw_df, region=Region.PT)

    pd.testing.assert_frame_equal(
        cleaned_df.fillna(np.nan).reset_index(drop=True),
        pt_life_expectancy_expected_json.fillna(np.nan).reset_index(drop=True)
    )
