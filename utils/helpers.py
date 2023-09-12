"""
Functions to make graphs go here.
"""

import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from typing import Literal
import locale

locale.setlocale(locale.LC_ALL, '')

config = {
    'ratio': {
        'scale': 250,
        'normalized_scale': 150,
        'color': "green",
        'title': "Police to General Fund Ratio (expressed as percentage), {}"
    },
    'police': {
        'scale': 0.2,
        'normalized_scale': 400,
        'color': "lightblue",
        'title': "Police $ Per Capita, {}"
    },
    'general_fund': {
        'scale': 0.05,
        'normalized_scale': 300,
        'color': "yellow",
        'title': "General Fund $ Per Capita, {}"
    }
}

def minmax(series):
    return (series - series.min())/(series.max() - series.min())

def map_maker(
        expense: Literal["general_fund", "police", "ratio"] = "ratio", 
        year: int=2023,
        normalize: bool=True
        ):
    
    
    df = pd.read_csv("http://philadelphyinz.com/drop/budget_data_melted_UNCHECKED.csv").dropna()
    df = df.query("year==@year")

    if expense != 'ratio':
        upper_boundary = df[expense].describe()['75%']
        df = df.query(f'{expense} < @upper_boundary')
        raw_values = df[expense.lower()]/df['pop']
        formatted_values = df[expense].map(lambda c: locale.currency(c, grouping=True))
    else:
        raw_values = df['police']/df['general_fund']
        formatted_values = raw_values.map(lambda c: f"{round(c*100, 3)}%")

    if normalize:
        values = minmax(raw_values)*config[expense]['normalized_scale']
    else:
        values = raw_values*config[expense]['scale']
    cities = df['city'] + ", " + df['state']

    
    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df['longitude'],
        lat = df['latitude'],
        text = [f"{c}\n\n{v}" for v, c in zip(formatted_values, cities)],
        marker = dict(
            size = values,
            line_color="black",
            opacity=0.3,
            color=config[expense]['color'],
            line_width=1,
            sizemode = 'area'
        ),
    )
    )

    fig.update_layout(
            # showlegend = True,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
                lakecolor="lightblue",
            ),
            title=config[expense]['title'].format(year),
            plot_bgcolor="black",
        )

    return fig

def init_callbacks(app):
    """
    Adds provided callbacks to dash_app.
    """
    # callbacks
    @app.callback(
    Output("big-map", "figure"),
    [
        Input("expense-type", "value"),
        Input("year", "value"),
        Input("normalizer", "on")
        ],
)
    def update_map(expense, year, normalize):
        figure = map_maker(expense, year, normalize)
        return figure
    
