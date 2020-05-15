"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from .layout import html_layout

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

    # Prepare a DataFrame
    df = pd.read_csv('data/311-calls.csv', parse_dates=['created_date'])
    num_complaints = df['complaint_type'].value_counts()
    to_remove = num_complaints[num_complaints <= 20].index
    df.replace(to_remove, np.nan, inplace=True)

    # Custom HTML layout
    #dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[html.Div(className='container-fluid', children=[html.H2('Live Sentiment Analysis', style={'color':"#CECECE"}),
                                                        html.H3('Search:', style={'color':app_colors['text']}),
                                                  dcc.Input(id='sentiment_term',placeholder='Enter the text', value='', type='text', style={'color':app_colors['someothercolor']}),
                                                  ],
                 style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000}),
            dcc.Graph(
            id='histogram-graph',
            figure={
                'data': [
                    {
                        'x': df['complaint_type'],
                        'text': df['complaint_type'],
                        'customdata': df['unique_key'],
                        'name': '311 Calls by region.',
                        'type': 'histogram'
                    }
                ],
                'layout': {
                    'title': 'NYC 311 Calls category.',
                    'height': 600,
                    'padding': 150
                }
            }),

            create_data_table(df)
            ],
            style={'backgroundColor': app_colors['background'], 'margin-top':'-30px', 'height':'2000px',},
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
