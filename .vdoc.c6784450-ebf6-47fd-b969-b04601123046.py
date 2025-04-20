# type: ignore
# flake8: noqa
#
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load poverty data
poverty_data = pd.read_csv("data/clean_data/state_poverty.csv")

# Directory with state drug data CSVs
folder_path = "data/state_data"
files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# Loop through each state file and generate plots
for file in files:
    state_name = file.replace(".csv", "").title()
    
    # Read drug usage data
    df = pd.read_csv(os.path.join(folder_path, file))
    df = df.iloc[8:18, :]  # Age group rows only
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    # Rename columns for consistency
    df = df.rename(columns={df.columns[0]: "Age Group"})
    df["state"] = state_name

    # Reshape data for faceted bar plot
    drug_columns = df.columns[2:-1]  # exclude Age Group and state
    df_melted = df.melt(id_vars=["Age Group"], value_vars=drug_columns,
                        var_name="Substance", value_name="Usage (%)")

    # Get matching poverty info
    state_pov = poverty_data[poverty_data["name"] == state_name]

    # Set up subplots: 1 row, 2 columns
    subfig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.75, 0.25],
        specs=[[{"type": "xy"}, {"type": "xy"}]],
        subplot_titles=[f"{state_name} - Substance Use by Age", "Poverty Rates"]
    )

    # Drug usage bar plot (faceted manually)
    for substance in df_melted["Substance"].unique():
        df_sub = df_melted[df_melted["Substance"] == substance]
        subfig.add_trace(
            go.Bar(x=df_sub["Age Group"], y=df_sub["Usage (%)"], name=substance),
            row=1, col=1
        )

    # Poverty bar plot
    if not state_pov.empty:
        subfig.add_trace(
            go.Bar(
                x=["Total Poverty", "Child Poverty"],
                y=[state_pov.iloc[0]["total_pov"], state_pov.iloc[0]["child_pov"]],
                marker_color="crimson",
                name="Poverty"
            ),
            row=1, col=2
        )

    subfig.update_layout(
    title_text=f"{state_name}: Drug Use vs Poverty",
    showlegend=True,
    height=600,
    width=1200,
    legend_title="Drug Type",
    legend=dict(
        orientation="v",
        x=1.02,  # Push legend just outside the right edge
        y=1,
        bgcolor="rgba(255,255,255,0.7)",
        bordercolor="black",
        borderwidth=1
    )
    )

    subfig.update_xaxes(title_text="Age Groups", row=1, col=1)
    subfig.update_yaxes(title_text="Usage (%)", row=1, col=1)
    subfig.update_yaxes(title_text="Poverty Rate (%)", row=1, col=2)

    subfig.show()

#
#
#
#
#
