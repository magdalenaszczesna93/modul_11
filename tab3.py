import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def render_tab(df):

#     grouped = df[df['total_amt']>0].pivot_table(index='Store_type',columns='Pokolenie',values='total_amt',aggfunc='sum').assign(
#         _sum=lambda x: x['silent generation']+x['baby boomers']+x['pokolenie X']+x['milenialsi']+x['pokolenie Z']).sort_values(by='_sum').round(2)


    traces = []
#     for col in ['silent generation','baby boomers','pokolenie X','milenialsi','pokolenie Z']:
#         traces.append(go.Bar(x=grouped[col],y=grouped.index,orientation='h',name=col))

    data = traces
    fig = go.Figure(data=data,layout=go.Layout(title='Kanały sprzedaży według pokolenia',barmode='stack'))

#     grouped = df[df['total_amt']>0].groupby('Store_type')['total_amt'].sum().round(2).unstack()

    layout = html.Div([html.H1('Kanały sprzedaży',
                                style={'text-align':'center'}),
                        html.Div([html.Div([dcc.Dropdown(id='store_dropdown', 
                                                        options=[{'label':Store_type,
                                                                'value':Store_type} for Store_type in df['Store_type'].unique()], 
                                                        value=df['Store_type'].unique()[0]),
                                            dcc.Graph(id='pie-store-type')],
                                            style={'width':'50%'}),
                                html.Div([dcc.Graph(id='barh-pokolenie'
                                , figure=fig 
                                )],
                                        style={'width':'50%'})],
                                style={'display':'flex'}),
                        html.Div(id='temp-out')])
    return layout
