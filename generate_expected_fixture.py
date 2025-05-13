"""Generates the expected fixture for the life expectancy dataset."""

import pandas as pd
from life_expectancy.cleaning import clean_data

input_path = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"
output_path = "life_expectancy/tests/fixtures/eu_life_expectancy_expected.csv"

# Load the input fixture and clean the data
df_sample = pd.read_csv(input_path, sep="\t")
df_cleaned = clean_data(df_sample, region="PT")
df_cleaned.to_csv(output_path, index=False)

print(f"Expected fixture criado: {output_path}")
