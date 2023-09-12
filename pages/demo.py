from dash import html, dash_table, dcc, register_page
from utils.helpers import map_maker
import dash_daq as daq

register_page(__name__, "/")

map_ = map_maker()

layout = html.Div(
        className="wrapper",
        children=[
            html.H1("US General Funds and Police Budgets, 2018-2022"),
            html.Div(
                className='menu-block',
                # menus
                children=[
                    html.Span(
                        "Fund to display...",
                        className="menu-label"
                        ),
                    html.Div(
                        dcc.Dropdown(
                            className="menu",
                            id="expense-type",
                            value="ratio",
                            options=[
                                {
                                    "label": "Police",
                                    "value": "police"
                                },
                                {
                                    "label": "General Fund",
                                    "value": "general_fund"
                                },
                                {
                                    "label": "Police to General Fund Ratio",
                                    "value": "ratio"
                                }
                            ]
                        )
                    ),
                    html.Span(
                        "Year...",
                        className="menu-label"
                        ),
                    html.Div(
                        dcc.Dropdown(
                            className="menu",
                            id="year",
                            value=2022,
                            options=[
                                {"label": c, "value": c} for c in range(2018,2023)
                            ]
                        )
                    ),
                    html.Span(
                        "Toggle normalization...",
                        className="menu-label"
                        ),
                    html.Div(
                        daq.BooleanSwitch(
                            className="menu",
                            id="normalizer",
                            color="black",
                            on=True
                        )
                    )

                ]
            ),
            html.Div(
                # graphs
                children=[
                    html.Div(
                        dcc.Graph(id="big-map", figure=map_)),
                ]
            )
            
        ],
    )