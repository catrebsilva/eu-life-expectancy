"""Pytest configuration file."""

from pathlib import Path
import pandas as pd
import pytest
from . import FIXTURES_DIR

@pytest.fixture(scope="session")
def pt_life_expectancy_expected_tsv() -> pd.DataFrame:
    """Expected cleaned output from TSV data."""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")

@pytest.fixture(scope="session")
def pt_life_expectancy_expected_json() -> pd.DataFrame:
    """Expected cleaned output from JSON data."""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected_from_json.csv")

@pytest.fixture(scope="session")
def eurostat_life_expectancy_json_path() -> Path:
    """Path to the Eurostat JSON file (not zipped)."""
    return Path("life_expectancy/data/eurostat_life_expect.json")

@pytest.fixture(scope="session")
def eu_life_expectancy_tsv_path() -> Path:
    """Path to the raw TSV file."""
    return FIXTURES_DIR / "eu_life_expectancy_raw.tsv"
