"""Instantiate a Dash app."""
import datetime
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from .layout import html_layout
import sqlite3
import plotly.express as px

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
    pol=list()
    f_list=df['sentiment'].to_list()
    for l in f_list:
        if(l>0):
            pol.append(1)
        if(l<0):
            pol.append(-1)
        if(l==0):
            pol.append(0)
    df['polarity']=pol

    twdf = pd.read_sql('select * from twsentiment', conn)
    #twdf['date'] = pd.to_datetime(df['unix'])
    num_entries = twdf['id'].value_counts()

    # Custom HTML layout
    #dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[

            html.Div(
                dcc.Graph(
                    id='line-graph',
                    config={'displayModeBar': False},
                    animate= True,
                    figure=px.line(df,
                                   x='date',
                                   y='sentiment',
                                   title='YOUTUBE sentiment analysis',
                                   ),
                    style={'padding': 25, 'height':600}
                )
            ),

             html.Div(
                dcc.Graph(
                    id='bar-graph',
                    figure={
                        'data': [
                            {
                                'x': df['date'],
                                'y': df['sentiment'],
                                'name': 'YOUTUBE sentiment analysis',
                                'type': 'bar'
                            }
                         ],
                        'layout': {
                                'title': 'YOUTUBE sentiment analysis.',
                                'height': 600,
                                'padding': 150
                        }
                    }),
                ),

                html.Div(
                dcc.Graph(
                    id='histo-graph',
                    config={'displayModeBar': False},
                    animate= True,
                    figure=px.histogram(df,
                                   y='date',
                                   x='sentiment',
                                   title='YOUTUBE sentiment analysis',
                                   ),
                    style={'padding': 25, 'height':600}
                )
            ),

            html.Div(
                dcc.Graph(
                    id='scatter-graph',
                    config={'displayModeBar': False},
                    animate= True,
                    figure=px.scatter(df,
                                   x='date',
                                   y='sentiment',
                                   title='YOUTUBE sentiment analysis',
                                   ),
                    style={'padding': 25, 'height':600}
                )
            ),

            html.Div(
                dcc.Graph(
                    id='pie-graph',
                    config={'displayModeBar': False},
                    animate= True,
                    figure=px.pie(df,
                                   values='sentiment',
                                   names='polarity',
                                   title='YOUTUBE sentiment analysis',
                                   ),
                    style={'padding': 25, 'height':1200}
                )
            ),

            ],

        id='dash-container',


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

'''@dash_app.callback(Output('dash-container', 'children'),
                  [Input('interval-component', 'n_intervals')])'''
