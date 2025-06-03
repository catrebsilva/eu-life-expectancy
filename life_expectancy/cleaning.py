"""Cleaning module for life expectancy data using Strategy pattern."""

import sys
from pathlib import Path
import pandas as pd

from life_expectancy.region_enum import Region
from life_expectancy.data_loader.strategy import DataLoadingStrategy
from life_expectancy.data_loader.tsv_loader import TSVLoader
from life_expectancy.data_loader.json_loader import JSONLoader

def load_data(file_path: Path, loader: DataLoadingStrategy) -> pd.DataFrame:
    """Load raw life expectancy data using the selected strategy."""
    return loader.load(file_path)

def clean_data(life_expectancy_raw_df: pd.DataFrame, region: Region = Region.PT) -> pd.DataFrame:
    """Clean and reshape raw data, filtering by region."""

    if "unit,sex,age,geo\\time" in life_expectancy_raw_df.columns:
        # Format: TSV
        df_melted = life_expectancy_raw_df.melt(
            id_vars="unit,sex,age,geo\\time",
            var_name="year",
            value_name="value"
        )
        df_split = df_melted["unit,sex,age,geo\\time"].str.split(",", expand=True)
        df_split.columns = ["unit", "sex", "age", "region"]
        df_base = df_melted.drop(columns=["unit,sex,age,geo\\time"])
        df_combined = pd.concat([df_split, df_base], axis=1)
        df_combined["year"] = df_combined["year"].astype(int)
        df_combined["value"] = pd.to_numeric(
            df_combined["value"].str.extract(r"(\d+(?:\.\d+)?)")[0],
            errors="coerce"
        )
    else:
        # Format: JSON
        df_combined = life_expectancy_raw_df.rename(columns={
            "country": "region",
            "life_expectancy": "value"
        })

    df_combined.replace("", pd.NA, inplace=True)

    df_clean = df_combined.dropna(subset=["value"])

    df_filtered = df_clean[df_clean["region"] == region.name]

    return df_filtered

def save_data(df: pd.DataFrame, region: Region = Region.PT) -> None:
    """Save the cleaned data as CSV for the selected region."""
    output_path = Path(__file__).parent / "data" / f"{region.name.lower()}_life_expectancy.csv"
    df.to_csv(output_path, index=False)

def main(
    region: Region = Region.PT,
    file_path: Path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv",
    loader: DataLoadingStrategy = TSVLoader()
) -> pd.DataFrame:
    """Run the full cleaning pipeline using a given loading strategy."""
    raw_df = load_data(file_path, loader)
    cleaned_df = clean_data(raw_df, region)
    save_data(cleaned_df, region)
    return cleaned_df

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument(
        "--region", type=str, default="PT",
        help="Country code to filter data (e.g. PT, BE, DE)"
    )
    parser.add_argument(
        "--format", type=str, default="tsv", choices=["tsv", "json"],
        help="Format of the input file (tsv or json)"
    )
    args = parser.parse_args()

    try:
        selected_region = Region[args.region]
    except KeyError:
        print(f"Invalid region code: {args.region}. Must be one of: {[r.name for r in Region]}")
        sys.exit(1)

    if args.format == "json":
        input_path = Path(__file__).parent / "data" / "eurostat_life_expectancy.json"
        selected_loader = JSONLoader()
    else:
        input_path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
        selected_loader = TSVLoader()

    main(region=selected_region, file_path=input_path, loader=selected_loader)
