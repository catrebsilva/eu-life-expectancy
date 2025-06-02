"""Generates the input fixture for the life expectancy dataset."""

import pandas as pd

INPUT_PATH = "life_expectancy/data/eu_life_expectancy_raw.tsv"
OUTPUT_PATH = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"
COLUMN_NAME = "unit,sex,age,geo\\time"

# Load the input data and create a filtered sample with multiple countries
df = pd.read_csv(INPUT_PATH, sep="\t")
sample_df = df[df[COLUMN_NAME].str.contains("PT|FR|DE|IT|ES", regex=True)].copy()
sample_df.to_csv(OUTPUT_PATH, sep="\t", index=False)

print(f"Input fixture created: {OUTPUT_PATH}")
