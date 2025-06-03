"""Concrete data loader strategy for TSV files."""

from pathlib import Path
import pandas as pd
from life_expectancy.data_loader.strategy import DataLoadingStrategy

# pylint: disable=too-few-public-methods
class TSVLoader(DataLoadingStrategy):
    """Strategy for loading TSV life expectancy data."""

    def load(self, file_path: Path) -> pd.DataFrame:
        """Load a TSV file into a pandas DataFrame."""
        return pd.read_csv(file_path, sep="\t")
