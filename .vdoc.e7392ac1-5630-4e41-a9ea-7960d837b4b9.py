# type: ignore
# flake8: noqa
#
import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv("data/state_data/UNITED STATES.csv")
df = df.iloc[8:18,:]
fig = go.Figure()
columns = columns = ["State: UNITED STATES", 
           "All Substances", 
           "Alcohol Only", 
           "Alcohol with secondary drug", 
           "Heroin", 
           "Other opiates", 
           "Cocaine (smoked)", 
           "Cocaine (other route)", 
           "Marijuana", 
           "Amphetamines", 
           "Other stimulants", 
           "Tranquilizers", 
           "Sedatives", 
           "Hallucinogens", 
           "PCP", 
           "Inhalants", 
           "Other/Unknown"]

df_melted = df.melt(id_vars=["State: UNITED STATES"], 
                    value_vars=columns[2:], 
                    var_name="Substance", 
                    value_name="Value")

# Plot with facet per substance
fig = px.bar(df_melted, 
             x="State: UNITED STATES", 
             y="Value", 
             facet_col="Substance", 
             facet_col_wrap=4, 
             title="Substance Use by Age Group Across the US",
             labels={"Value": "Usage (%)", "State: UNITED STATES": "Age Groups"},
             height=1200)

fig.update_layout(showlegend=False)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))  # Clean facet labels

fig.show()

#
#
#
import pandas as pd
import os

# Path to the folder where all state CSVs are stored
folder_path = "data/state_data"

# Get all CSV files in that folder
files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# Initialize an empty list to store dataframes
all_states = []

for file in files:
    # Read the current state dataframe
    state_df = pd.read_csv(os.path.join(folder_path, file))
    
    # Extract state name from filename (assuming the filename represents the state)
    state_name = file.replace(".csv", "").title()  # You can adjust this depending on how the filenames are structured
    state_df["State"] = state_name
    
    # Extract relevant rows (age group breakdown)
    state_df = state_df.iloc[8:20].copy()  # Rows 8-20, adjust if needed
    
    # Append the dataframe for this state to the list
    all_states.append(state_df)

# Combine all states into one dataframe
df_drugs_all = pd.concat(all_states, ignore_index=True)

# Drop the unnecessary column (Unnamed column)
df = df_drugs_all.drop(columns=["Unnamed: 0"])
df = df.drop(df.columns[18:], axis=1)


df = df.rename(columns={"State: GEORGIA": "Age Group"})
df = df.rename(columns={"State": "state"})

df.columns

#
#
#

poverty_data = pd.read_csv("data/clean_data/state_poverty.csv")
combined_data = pd.merge(df, poverty_data, left_on="state", right_on="name", how="right")
print(combined_data.head())

# # Bar chart
fig = px.scatter(
    long_df,
    x="child_pov",
    y="Avg Usage (%)",
    color="Substance",
    facet_wrap="Substance",
    title="Drug Usage vs Child Poverty Rate (by Substance)",
    hover_name="State",
    height=1200,
    width=1000
)

# fig.show()
#
#
#
import plotly.express as px


#
#
#
