# -- From https://dash.plotly.com/tutorial
from dash import html, dash_table, dcc, callback, Output, Input, register_page, ctx
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from defaultlayouts import globalconstants
from plotly_v0 import my_plot

register_page(module=__name__,
              name="Sample Graph",
              title='Sample Graph')

load_figure_template(["bootstrap", "bootstrap_dark"])

# ----------------------------------------------------------------------------------------------

# Load historical data
def load_data(filename:str):
    with open(f"{filename}.json") as f:
        data = json.load(f)  # Parse the entire JSON array
    return pd.DataFrame(data)

def get_last_entry(filename):
    with open(f"{filename}.json", "r") as file:
        data = json.load(file)
    sorted_keys = sorted(data.keys(), key=int)
    last_key = sorted_keys[-1]
    last_entry = data[last_key]
    return pd.DataFrame([last_entry])

def create_gauge(value, title, big: bool):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value * 100,
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gold"},
                {'range': [75, 100], 'color': "crimson"}
            ],
        },
        delta={'reference': value, 'relative': False},
        title={'text': title, 'font': {'size': 20}}
    ))

    if not big:
        fig.update_layout(
            width=400, height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            paper_bgcolor="white",
            font={'color': "darkblue", 'family': "Arial"}
        )
    else:
        fig.update_layout(
            width=600, height=500,
            margin=dict(t=50, b=50, l=50, r=50),
            paper_bgcolor="white",
            font={'color': "darkblue", 'family': "Arial"}
        )

    return fig

# Load data once
legislative_df = get_last_entry("Legislative")
media_df = get_last_entry("Media")
latest_legislative_data = legislative_df.iloc[-1]
latest_media_data = media_df.iloc[-1]

risk_gauge = create_gauge(latest_legislative_data["score"]*0.6 + latest_media_data["score"]*0.4, "Regulatory Risk Index",True)
legislative_gauge = create_gauge(latest_legislative_data["score"], "Legislative Activity Score", False)
media_gauge = create_gauge(latest_media_data["score"], "Media Activity Score", False)
legislative_plot = my_plot("Legislative")
media_plot = my_plot("Media")


# ----------------------------------------------------------------------------------------------




# App layout
layout = [
    html.Div([
        dbc.Row([
            html.Div('Example Graph', className="text-center fs-3"),
            html.Div([
                "This example, taken from ",
                html.A("https://dash.plotly.com/tutorial", 
                    href="https://dash.plotly.com/tutorial", target="_blank"),
                " shows how controls can be duplicated on a custom pop-up sidebar"
            ])
        ]),
        dbc.Row(
            [
                dbc.Col([
                    dcc.Graph(figure=risk_gauge, id='my-first-graph-final')
                    ],
                    id='col-graph',
                    md=6,
                ),
            ],
            className='dbc',
        ), 
    ], className="page-body"),
]
