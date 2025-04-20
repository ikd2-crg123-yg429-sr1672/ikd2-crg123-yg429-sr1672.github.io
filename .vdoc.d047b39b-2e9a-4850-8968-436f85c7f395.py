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
%pip install dash
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Load poverty data
poverty_data = pd.read_csv("data/clean_data/state_poverty.csv")
poverty_data["code"] = poverty_data["code"].str.upper()  # Ensure state codes are uppercase

# Create US map with poverty rates
fig_map = px.choropleth(
    poverty_data,
    locations="code",
    locationmode="USA-states",
    color="total_pov",
    hover_name="name",
    color_continuous_scale="Reds",
    scope="usa",
    title="Click a State to See Substance Use vs Poverty"
)

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # for deployment

# Layout
app.layout = html.Div([
    html.H2("US Substance Use & Poverty Dashboard"),
    dcc.Graph(id="us-map", figure=fig_map),
    dcc.Graph(id="state-details")
])

# Callback to update plot based on state click
@app.callback(
    Output("state-details", "figure"),
    Input("us-map", "clickData")
)
def update_state_plot(clickData):
    if not clickData:
        return go.Figure().update_layout(title="Click on a state to view data.")

    state_code = clickData["points"][0]["location"]
    state_name = poverty_data[poverty_data["code"] == state_code]["name"].values[0]
    file_path = f"data/state_data/{state_name.lower()}.csv"

    if not os.path.exists(file_path):
        return go.Figure().update_layout(title=f"No drug usage data found for {state_name}")

    # Load drug usage data
    df = pd.read_csv(file_path)
    df = df.iloc[8:18, :].drop(columns=["Unnamed: 0"], errors="ignore")
    df = df.rename(columns={df.columns[0]: "Age Group"})
    df["state"] = state_name
    drug_columns = df.columns[2:-1]
    df_melted = df.melt(id_vars=["Age Group"], value_vars=drug_columns,
                        var_name="Substance", value_name="Usage (%)")
    state_pov = poverty_data[poverty_data["name"] == state_name]

    # Create subplot
    subfig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.75, 0.25],
        specs=[[{"type": "xy"}, {"type": "xy"}]],
        subplot_titles=[f"{state_name} - Substance Use by Age", "Poverty Rates"]
    )

    # Add drug use bars
    for substance in df_melted["Substance"].unique():
        df_sub = df_melted[df_melted["Substance"] == substance]
        subfig.add_trace(
            go.Bar(x=df_sub["Age Group"], y=df_sub["Usage (%)"], name=substance),
            row=1, col=1
        )

    # Add poverty bars
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

    # Final layout tweaks
    subfig.update_layout(
        title=f"{state_name}: Drug Use vs Poverty",
        height=600,
        width=1200,
        showlegend=True,
        legend_title="Drug Type",
        legend=dict(
            orientation="v",
            x=1.02,
            y=1,
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="black",
            borderwidth=1
        )
    )
    subfig.update_xaxes(title_text="Age Groups", row=1, col=1)
    subfig.update_yaxes(title_text="Usage (%)", row=1, col=1)
    subfig.update_yaxes(title_text="Poverty Rate (%)", row=1, col=2)

    return subfig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

#
#
#
