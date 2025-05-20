import pandas as pd

df = pd.read_csv("Foundations/lp-foundations/assignments/life_expectancy/data/eu_life_expectancy_raw.tsv", sep="\t")
geo_series = df["unit,sex,age,geo\\time"].str.split(",", expand=True)[3]
unique_regions = sorted(geo_series.dropna().unique())

for region in unique_regions:
    print(f"    {region} = \"{region}\"")
