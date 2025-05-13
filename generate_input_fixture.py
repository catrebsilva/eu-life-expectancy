"""Generates the input fixture for the life expectancy dataset."""

import pandas as pd

input_path = "life_expectancy/data/eu_life_expectancy_raw.tsv"
output_path = "life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv"

# Load the input fixture and create a sample with several countries
df = pd.read_csv(input_path, sep="\t")
col = "unit,sex,age,geo\\time"
sample_df = df[df[col].str.contains("PT|FR|DE|IT|ES", regex=True)].copy()
sample_df.to_csv(output_path, sep="\t", index=False)

print(f"Input fixture criado: {output_path}")
