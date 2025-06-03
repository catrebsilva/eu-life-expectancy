"""Strategy interface and context class for loading data."""

from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd

# pylint: disable=too-few-public-methods
class DataLoadingStrategy(ABC):
    """Interface for loading data."""

    @abstractmethod
    def load(self, file_path: Path) -> pd.DataFrame:
        """Load data from file."""
        raise NotImplementedError

class DataReader:
    """Uses a loading strategy to read data."""

    def __init__(self, strategy: DataLoadingStrategy) -> None:
        """Init with strategy."""
        self._strategy = strategy

    def set_strategy(self, strategy: DataLoadingStrategy) -> None:
        """Update the strategy."""
        self._strategy = strategy

    def read(self, file_path: Path) -> pd.DataFrame:
        """Read data using current strategy."""
        return self._strategy.load(file_path)
