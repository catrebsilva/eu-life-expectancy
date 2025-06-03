"""Concrete data loader strategy for JSON files."""

from pathlib import Path
import pandas as pd
from life_expectancy.data_loader.strategy import DataLoadingStrategy

# pylint: disable=too-few-public-methods
class JSONLoader(DataLoadingStrategy):
    """Strategy for loading JSON life expectancy data."""
    def load(self, file_path: Path) -> pd.DataFrame:
        """Load a JSON file into a pandas DataFrame."""
        return pd.read_json(file_path)
