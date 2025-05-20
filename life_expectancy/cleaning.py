"""Cleaning module for life expectancy data"""

from pathlib import Path
import pandas as pd
from life_expectancy.region_enum import Region


def load_data(file_path: Path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv") -> pd.DataFrame:
    """Load raw life expectancy data from TSV file."""
    return pd.read_csv(file_path, sep="\t")


def clean_data(life_expectancy_raw_df: pd.DataFrame, region: Region = Region.PT) -> pd.DataFrame:
    """Clean and reshape raw data, filtering by region."""
    df_melted = life_expectancy_raw_df.melt(
        id_vars="unit,sex,age,geo\\time",
        var_name="year",
        value_name="value"
    )

    df_columns_splitted = df_melted["unit,sex,age,geo\\time"].str.split(",", expand=True)
    df_columns_splitted.columns = ["unit", "sex", "age", "region"]

    df_base = df_melted.drop(columns=["unit,sex,age,geo\\time"])
    df_combined = pd.concat([df_columns_splitted, df_base], axis=1)

    df_combined["year"] = df_combined["year"].astype(int)
    df_combined["value"] = pd.to_numeric(
        df_combined["value"].str.extract(r"(\d+(?:\.\d+)?)")[0],
        errors="coerce"
    )

    df_clean = df_combined.dropna(subset=["value"])
    df_filtered = df_clean[df_clean["region"] == region.value]

    return df_filtered


def save_data(df: pd.DataFrame, region: Region = Region.PT) -> None:
    """Save the cleaned data as CSV for the selected region."""
    output_path = Path(__file__).parent / "data" / f"{region.value.lower()}_life_expectancy.csv"
    df.to_csv(output_path, index=False)


def main(region: Region = Region.PT) -> pd.DataFrame:
    """Run the full cleaning pipeline for a given region."""
    raw_df = load_data()
    cleaned_df = clean_data(raw_df, region)
    save_data(cleaned_df, region)
    return cleaned_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument("--region", type=str, default="PT", help="Country code to filter data (e.g. PT, BE, DE)")
    args = parser.parse_args()

    try:
        selected_region = Region[args.region]  # converte string para Region enum
    except KeyError:
        print(f"Invalid region code: {args.region}. Must be one of: {[r.name for r in Region]}")
        exit(1)

    main(selected_region)
