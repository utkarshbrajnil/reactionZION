"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from .layout import html_layout
import sqlite3

app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}


def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashapp/',
                         external_stylesheets=['/static/dist/css/styles.css',
                                               'https://fonts.googleapis.com/css?family=Lato']
                         )

    #connect to the main database
    conn = sqlite3.connect('data/alldata.db', isolation_level=None, check_same_thread=False)
    c = conn.cursor()

    # Prepare a DataFrame
    df = pd.read_sql('select * from sentiment', conn)
    df['date'] = pd.to_datetime(df['unix'])
    num_entries = df['id'].value_counts()


    # Custom HTML layout
    #dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[dcc.Graph(
            id='histogram-graph',
            figure={
                'data': [
                    {
                        #'x': df['date'],
                        'y': df['sentiment'],
                        'text': df['date'],
                        'name': 'YOUTUBE sentiment analysis.',
                        'type': 'histogram'
                    }
                ],
                'layout': {
                    'title': 'YOUTUBE sentiment analysis.',
                    'height': 600,
                    'padding': 150
                }
            }),

            create_data_table(df)
            ],

        id='dash-container'
    )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id='database-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        page_size=300
    )
    return table
