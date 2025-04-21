"""Cleaning module for life expectancy data.

This module loads, cleans and saves life expectancy data filtered by region.
"""

from pathlib import Path
import pandas as pd


def load_data() -> pd.DataFrame:
    """Load original data from the file"""
    file_path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    return pd.read_csv(file_path, sep="\t")


def _clean_data(df: pd.DataFrame, region: str = "PT") -> pd.DataFrame:
    """Cleans and filters data for a specific region"""
    df_long = df.melt(id_vars="unit,sex,age,geo\\time", var_name="year", value_name="value")

    split_cols = df_long["unit,sex,age,geo\\time"].str.split(",", expand=True)
    split_cols.columns = ["unit", "sex", "age", "region"]

    df_long = df_long.drop(columns=["unit,sex,age,geo\\time"])
    df_long = pd.concat([split_cols, df_long], axis=1)

    df_long["year"] = df_long["year"].astype(int)
    df_long["value"] = df_long["value"].str.extract(r"(\d+(?:\.\d+)?)")[0]
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    df_long = df_long.dropna(subset=["value"])
    df_filtered_by_region = df_long[df_long["region"] == region]

    return df_filtered_by_region


def save_data(df: pd.DataFrame, region: str = "PT") -> None:
    """Guarda os dados limpos num ficheiro CSV."""
    output_path = Path(__file__).parent / "data" / f"{region.lower()}_life_expectancy.csv"
    df.to_csv(output_path, index=False)


def main(region: str = "PT") -> pd.DataFrame:
    """Função principal que é usada pelo teste. Executa o pipeline completo."""
    raw_df = load_data()
    cleaned_df = _clean_data(raw_df, region)
    save_data(cleaned_df, region)
    return cleaned_df


clean_data = main


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument("--region", type=str, default="PT", help="Country code to filter data")
    args = parser.parse_args()
    main(args.region)
