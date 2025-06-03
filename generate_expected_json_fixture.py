"""Generates the expected output fixture (CSV) from the JSON ZIP file."""

import zipfile
import json
from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region_enum import Region

INPUT_ZIP_PATH = Path("life_expectancy/tests/fixtures/eurostat_life_expect.zip")
JSON_FILENAME = "eurostat_life_expect.json"
OUTPUT_CSV_PATH = Path("life_expectancy/tests/fixtures/pt_life_expectancy_expected_from_json.csv")

with zipfile.ZipFile(INPUT_ZIP_PATH, "r") as archive:
    with archive.open(JSON_FILENAME) as json_file:
        raw_data = json.load(json_file)

df = pd.DataFrame(raw_data)
df_cleaned = clean_data(df, region=Region.PT)

df_cleaned.to_csv(OUTPUT_CSV_PATH, index=False)
