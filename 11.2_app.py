import dash
from dash import dcc
from dash import html
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objs as go
# from dash_app import app as application
from dash.dependencies import Input, Output

app = dash.Dash()
data = [go.Scatter(x=[1,2,3,4], y=[10,20,30,40])]
layout = go.Layout(title='Pierwszy wykres', width=600, height=600)
fig = go.Figure(data=data, layout=layout)
app.layout = html.Div(children=[
            html.H1('Mój dashboard',style={'margin':'auto'}),
            html.Div('Tu pojawi się content',style={'color':'red'}), 
            dcc.Graph(id='first-graph'),
            html.Label('Slider'),
            html.Div([dcc.Slider(id='my-slider', min=1, max=4, step=1, value=1)], style={'width':'400px'})])

@app.callback(Output(component_id='first-graph', component_property='figure'),[Input('my-slider', 'value')])

def update_figure(max_range):
    data = [go.Scatter(x=[1,2,3,4], y=[10,20,30,40])]
    layout = go.Layout(title='Pierwszy wykres', width=600, height=300, xaxis=dict(range=[1,max_range]))
    fig = go.Figure(data=data, layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    

