"""Cleaning module for life expectancy data"""

from pathlib import Path
import pandas as pd

def load_data(file_path: Path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv") -> pd.DataFrame:
    """Load the life expectancy data from a TSV file."""
    data = pd.read_csv(file_path, sep="\t")
    return data

def clean_data(life_expectancy_raw_df: pd.DataFrame, region: str = "PT") -> pd.DataFrame:
    """Clean and reshape raw data, filtering by region."""
    df_melted = life_expectancy_raw_df.melt(
        id_vars="unit,sex,age,geo\\time",
        var_name="year",
        value_name="value"
    )

    df_columns_splitted = df_melted["unit,sex,age,geo\\time"].str.split(",", expand=True)
    df_columns_splitted.columns = ["unit", "sex", "age", "region"]
    df_dropped_original = (df_melted.drop(columns=["unit,sex,age,geo\\time"])
    )
    df_combined = pd.concat(
        [df_columns_splitted, df_dropped_original], axis=1
    )

    df_combined["year"] = df_combined["year"].astype(int)
    df_combined["value"] = pd.to_numeric(
        df_combined["value"].str.extract(r"(\d+(?:\.\d+)?)")[0],
        errors="coerce"
    )

    df_valid_values = df_combined.dropna(subset=["value"])

    df_filtered = df_valid_values[df_valid_values["region"] == region]

    return df_filtered

def save_data(df: pd.DataFrame, region: str = "PT") -> None:
    """Save the cleaned data as CSV for the selected region."""
    output_path = Path(__file__).parent / "data" / f"{region.lower()}_life_expectancy.csv"
    df.to_csv(output_path, index=False)

def main(region: str = "PT") -> pd.DataFrame:
    """Run the full cleaning pipeline for a given region."""
    raw_df = load_data()
    cleaned_df = _clean_data(raw_df, region)
    save_data(cleaned_df, region)
    return cleaned_df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument("--region", type=str, default="PT", help="Country code to filter data")
    args = parser.parse_args()
    main(args.region)
