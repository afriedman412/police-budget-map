
from utils.helpers import init_callbacks
from dash import Dash, html, page_container
from dash.dcc import Location
import os
import connexion

def init_app():
    """
    Construct core Flask application with embedded Dash app.
    """
    dir_ = os.path.abspath(os.path.dirname(__file__))
    connex_app = connexion.App(__name__, specification_dir=dir_)
    app = connex_app.app
    # app.config.from_pyfile('config/config.py')
    return app

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        __name__,
        server=server,
        use_pages=True,
        pages_folder="pages",
        external_stylesheets=[
            '/assets/stylesheet.css',
        ]
    )
    dash_app.layout = html.Div([
        Location(id='url', refresh=True),
        page_container
    ])
    init_callbacks(dash_app)

    return dash_app.server

def combine_app():
    app = init_app()
    with app.app_context():
        app = init_dashboard(app)

    return app

