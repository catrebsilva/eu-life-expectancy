"""Generates the input JSON fixture inside a ZIP archive."""

import zipfile
from pathlib import Path
import pandas as pd

INPUT_JSON_PATH = Path("life_expectancy/data/eurostat_life_expect.json")
OUTPUT_ZIP_PATH = Path("life_expectancy/tests/fixtures/eurostat_life_expect.zip")
JSON_FILENAME = "eurostat_life_expect.json"

COUNTRIES = ["PT", "FR", "DE", "IT", "ES"]

df = pd.read_json(INPUT_JSON_PATH)

df_filtered = df[df["country"].isin(COUNTRIES)].copy()

json_bytes = df_filtered.to_json(orient="records").encode("utf-8")

with zipfile.ZipFile(OUTPUT_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
    archive.writestr(JSON_FILENAME, json_bytes)
