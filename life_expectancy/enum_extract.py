"""Export region codes from EU life expectancy dataset as enum entries."""

from pathlib import Path
from typing import List
import pandas as pd

def extract_unique_region_codes(data_path: Path) -> List[str]:
    """Extract unique region codes from the dataset."""
    df = pd.read_csv(data_path, sep="\t")
    geo_series = df["unit,sex,age,geo\\time"].str.split(",", expand=True)[3]
    return sorted(geo_series.dropna().unique())

def main():
    """Print formatted Enum entries for each unique region code."""
    file_path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    region_codes = extract_unique_region_codes(file_path)
    for code in region_codes:
        print(f"{code} = \"{code}\"")

if __name__ == "__main__":
    main()
