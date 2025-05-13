"""Pytest configuration file"""
import pandas as pd
import pytest
from pathlib import Path

from . import FIXTURES_DIR

@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")

@pytest.fixture(scope="session")
def eu_life_expectancy_raw_fixture() -> pd.DataFrame:
    """Load the input fixture (sample with several countries)."""
    path = FIXTURES_DIR / "eu_life_expectancy_raw.tsv"
    return pd.read_csv(path, sep="\t")

@pytest.fixture(scope="session")
def eu_life_expectancy_expected_fixture() -> pd.DataFrame:
    """Load the expected fixture (expected result for PT)."""
    path = FIXTURES_DIR / "eu_life_expectancy_expected.csv"
    return pd.read_csv(path)
