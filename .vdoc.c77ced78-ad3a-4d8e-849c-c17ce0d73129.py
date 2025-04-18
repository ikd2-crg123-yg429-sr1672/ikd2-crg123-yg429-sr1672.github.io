# type: ignore
# flake8: noqa
#
#
#
#
import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import matplotlib.pyplot as plt

df = pd.read_csv("data/state_data/UNITED STATES.csv")
df = df.iloc[8:20,:]
fig = go.Figure()
columns = columns = ["State: UNITED STATES", 
        #    "All Substances", 
        #    "Alcohol Only", 
        #    "Alcohol with secondary drug", 
        #    "Heroin", 
        #    "Other opiates", 
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

df_melted = df.melt(id_vars=["Age Group"], 
                    value_vars=columns[2:], 
                    var_name="Substance", 
                    value_name="Value")

# Plot with facet per substance
fig = px.bar(df_melted, 
             x="Age Group", 
             y="Value", 
             facet_col="Substance", 
             facet_col_wrap=4, 
             title="Substance Use by Age Group",
             labels={"Value": "Usage (%)"},
             height=1200)

fig.update_layout(showlegend=False)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))  # Clean facet labels

fig.show()

#
#
#
#
#
