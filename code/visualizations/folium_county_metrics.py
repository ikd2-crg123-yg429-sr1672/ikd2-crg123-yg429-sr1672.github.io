import pandas as pd
import folium
import requests
import numpy as np

# Load and clean data
df = pd.read_csv("../../data/clean_data/joined_data.csv")
df["fips"] = df["fips"].astype(str).str.zfill(5)
df = df[df["mean_addiction_deaths"].notna()]
df = df.drop_duplicates(subset="fips", keep="first")
df["log_overdose"] = np.log1p(df["mean_addiction_deaths"])  # log(1 + x)

# Load GeoJSON
geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
geojson_data = requests.get(geojson_url).json()

# Merge CSV data into GeoJSON
fips_to_row = df.set_index("fips").to_dict("index")
for feature in geojson_data["features"]:
    fips = feature["id"]
    if fips in fips_to_row:
        for key, val in fips_to_row[fips].items():
            feature["properties"][key] = val

# Create base map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="CartoDB positron")

# Add choropleth (log scale)
_ = folium.Choropleth(
    geo_data=geojson_data,
    data=df,
    columns=["fips", "log_overdose"],
    key_on="feature.id",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.1,
    legend_name="Log(Overdose Deaths + 1)",
    nan_fill_color="white",
).add_to(m)

# Add tooltip
tooltip_fields = [
    "county_name",
    "mean_addiction_deaths",
    "total_pov",
    "unemployment_rate_2021",
    "census_2020_pop",
]

tooltip_aliases = [
    "County:",
    "Avg. Overdose Deaths:",
    "Poverty Rate (%):",
    "Unemployment Rate (%):",
    "Population:",
]

_ = folium.GeoJson(
    geojson_data,
    name="Detailed Tooltip",
    style_function=lambda x: {"fillOpacity": 0, "weight": 0},
    tooltip=folium.features.GeoJsonTooltip(
        fields=tooltip_fields, aliases=tooltip_aliases, localize=True
    ),
).add_to(m)

# Optional: Layer control
_ = folium.LayerControl().add_to(m)

_ = m.save("../../outputs/folium_map_draft.html")
m
