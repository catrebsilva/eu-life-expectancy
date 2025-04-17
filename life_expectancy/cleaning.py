"""Cleaning script for EU life expectancy data."""

from pathlib import Path
import pandas as pd

def clean_data(country_code: str = "PT") -> None:
    """Loads, cleans, filters and saves life expectancy data for the given country code."""
    raw_data = _load_raw_data()
    reshaped_data = _reshape_to_long_format(raw_data)
    cleaned_data = _clean_and_filter_data(reshaped_data, country_code)
    _save_cleaned_data(cleaned_data)
    print(f"✅ Dados de esperança média de vida para '{country_code}' guardados com sucesso!")


def _load_raw_data() -> pd.DataFrame:
    file_path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    return pd.read_csv(file_path, sep="\t")


def _reshape_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    split = df["unit,sex,age,geo\\time"].str.split(",", expand=True)
    split.columns = ["unit", "sex", "age", "region"]
    df = df.drop(columns=["unit,sex,age,geo\\time"])
    df = pd.concat([split, df], axis=1)
    return df.melt(id_vars=["unit", "sex", "age", "region"],
                   var_name="year", value_name="value")


def _clean_and_filter_data(df: pd.DataFrame, country_code: str) -> pd.DataFrame:
    df["year"] = df["year"].astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    df = df[df["region"] == country_code]
    print(f"After filter '{country_code}':", len(df))
    return df



def _save_cleaned_data(df: pd.DataFrame) -> None:
    output_path = Path(__file__).parent / "data" / "pt_life_expectancy.csv"
    df.to_csv(output_path, index=False)


if __name__ == "__main__":  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument(
        "--country",
        type=str,
        default="PT",
        help="Country code to filter data (default: PT)"
    )

    args = parser.parse_args()
    clean_data(args.country)
