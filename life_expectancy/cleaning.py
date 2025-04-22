"""Cleaning module for life expectancy data."""

# pylint: disable=missing-function-docstring

from pathlib import Path
import pandas as pd


def load_data() -> pd.DataFrame:
    file_path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    return pd.read_csv(file_path, sep="\t")


def _clean_data(life_expectancy_raw_df: pd.DataFrame, region: str = "PT") -> pd.DataFrame:

    df_with_year_cols_melted_to_rows = life_expectancy_raw_df.melt(
        id_vars="unit,sex,age,geo\\time",
        var_name="year",
        value_name="value"
    )

    df_split_1st_col_in_4cols = df_with_year_cols_melted_to_rows[
        "unit,sex,age,geo\\time"
    ].str.split(",", expand=True)
    df_split_1st_col_in_4cols.columns = ["unit", "sex", "age", "region"]
    df_after_removing_original_aggregated_col = (
        df_with_year_cols_melted_to_rows.drop(columns=["unit,sex,age,geo\\time"])
    )
    df_with_final_cols = pd.concat(
        [df_split_1st_col_in_4cols, df_after_removing_original_aggregated_col], axis=1
    )

    df_with_final_cols["year"] = df_with_final_cols["year"].astype(int)
    df_with_final_cols["value"] = pd.to_numeric(
        df_with_final_cols["value"].str.extract(r"(\d+(?:\.\d+)?)")[0],
        errors="coerce"
    )

    df_with_valid_values = df_with_final_cols.dropna(subset=["value"])

    df_filtered_by_region = df_with_valid_values[df_with_valid_values["region"] == region]

    return df_filtered_by_region


def save_data(df: pd.DataFrame, region: str = "PT") -> None:
    output_path = Path(__file__).parent / "data" / f"{region.lower()}_life_expectancy.csv"
    df.to_csv(output_path, index=False)


def main(region: str = "PT") -> pd.DataFrame:
    raw_df = load_data()
    cleaned_df = _clean_data(raw_df, region)
    save_data(cleaned_df, region)
    return cleaned_df


clean_data = main     #This is just to run correctly in test_cleaning.py


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument("--region", type=str, default="PT", help="Country code to filter data")
    args = parser.parse_args()
    main(args.region)
