import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def render_tab(df):
    day = dict(zip(df['tran_date'],df['tran_date'].dt.day_name()))
    df['week_day'] = df['tran_date'].map(day)
    grouped = df[df['total_amt']>0].groupby('week_day')['total_amt'].sum()
    fig = go.Figure(data=[go.Pie(labels=grouped.index,values=grouped.values)],layout=go.Layout(title='Udział kanału sprzedaży w dniach tygodnia'))

    layout = html.Div([html.H1('Kanały sprzedaży',
                                style={'text-align':'center'}),
                        html.Div([html.Div([dcc.Dropdown(id='store_dropdown', 
                                                        options=[{'label':Store_type,
                                                                'value':Store_type} for Store_type in df['Store_type'].unique()], 
                                                        value=df['Store_type'].unique()[0]),
                                            dcc.Graph(id='pie-store-type',
                                                        figure=fig)],
                                            style={'width':'40%'}),
                                html.Div([dcc.Graph(id='barh-pokolenie')],
                                        style={'width':'40%'})],
                                style={'display':'flex'}),
                        html.Div(id='temp-out')])
    return layout


def render_tab(df):
    layout = html.Div([html.H1('Sprzedaż globalna',
                                style={'text-align':'center'}),
                        html.Div([dcc.DatePickerRange(id='sales-range', 
                                                    start_date=df['tran_date'].min(),
                                                    end_date=df['tran_date'].max(), 
                                                    display_format='YYYY-MM-DD')],
                                style={'width':'100%','text-align':'center'}),
                        html.Div([html.Div([dcc.Graph(id='bar-sales')],
                                            style={'width':'50%'}),
                                            html.Div([dcc.Graph(id='choropleth-sales')],
                                                    style={'width':'50%'})],
                                style={'display':'flex'})])
    return layout