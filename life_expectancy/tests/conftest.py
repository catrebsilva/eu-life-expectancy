"""Pytest configuration file."""

import pandas as pd
import pytest

from . import FIXTURES_DIR

@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Load expected output for PT from full dataset."""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")

@pytest.fixture(scope="session")
def eu_life_expectancy_raw_fixture() -> pd.DataFrame:
    """Load the raw sample input fixture."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")

@pytest.fixture(scope="session")
def eu_life_expectancy_expected_fixture() -> pd.DataFrame:
    """Load the expected cleaned output for PT."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")
