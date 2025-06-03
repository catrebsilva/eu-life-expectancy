"""Generates the expected fixture for the life expectancy dataset."""

import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region_enum import Region

INPUT_PATH = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"
OUTPUT_PATH = "life_expectancy/tests/fixtures/eu_life_expectancy_expected.csv"

df_sample = pd.read_csv(INPUT_PATH, sep="\t")
df_cleaned = clean_data(df_sample, region=Region.PT)
df_cleaned.to_csv(OUTPUT_PATH, index=False)

print(f"Expected fixture created: {OUTPUT_PATH}")
