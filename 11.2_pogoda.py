# import dash
# from dash import dcc
# from dash import html
# import plotly.graph_objs as go
# from dash.dependencies import Input, Output
# import pandas as pd
# from plotly import tools
# import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from plotly import tools
import datetime as dt

df = pd.read_csv('dataexport_20200613T163949.csv',skiprows=9, index_col=0, parse_dates=True)

app = dash.Dash()

app.layout = html.Div(children=[html.H1('Pogoda we Wrocławiu', style={'text-align': 'center'}),
            dcc.Graph(id='wro-weather'), dcc.RangeSlider(id='date-slider',
                min=df.index.min().day, max=df.index.max().day, step=1,
                marks={date.day: date.strftime('%m-%d') for date in df.index.unique()},
                value=[df.index.min().day, df.index.max().day]),
            html.Div(id='hover-details', style={'text-align': 'center',
                'margin-top': '20px', 'font-weight': 'bold'})], style={'width': '80%', 'margin': 'auto'})


@app.callback(Output('wro-weather', 'figure'), [Input('date-slider', 'value')])
def update_heatmap(x_range):
    wro_temp = df.truncate(before=dt.datetime(2020, 6, x_range[0]),
                after=dt.datetime(2020, 6, x_range[1])+pd.Timedelta(hours=23))

    fig = tools.make_subplots(rows=1, cols=2, subplot_titles=[
            'Temperatura', 'Opady'], shared_yaxes=True)

    fig.append_trace(go.Heatmap(x=wro_temp.index.hour, y=wro_temp.index.weekday.map(
        {0: 'Poniedziałek', 1: 'Wtorek', 2: 'Środa', 3: 'Czwartek', 4: 'Piątek',
        5: 'Sobota', 6: 'Niedziela'}), z=wro_temp['Wrocław Temperature [2 m elevation corrected]'].tolist(),
        colorscale='Jet', showscale=False), 1, 1)
    fig.append_trace(go.Heatmap(x=wro_temp.index.hour, y=wro_temp.index.weekday.map(
        {0: 'Poniedziałek', 1: 'Wtorek', 2: 'Środa',3: 'Czwartek', 4: 'Piątek', 5: 'Sobota',
        6: 'Niedziela'}), z=wro_temp['Wrocław Precipitation Total'].tolist(),
        colorscale='Cividis', showscale=False), 1, 2)
    return fig

@app.callback(Output('hover-details', 'children'),
              [Input('wro-weather', 'hoverData')])
def update_hover_details(hoverData):
    dpoint = hoverData['points'][0]
    if dpoint['curveNumber'] == 0:
        return f"{dpoint['y']}: temperatura powietrza o godzinie {dpoint['x']} wynosiła {round(dpoint['z'],2)}"
    elif dpoint['curveNumber'] == 1:
        return f"{dpoint['y']}: opady o godzinie {dpoint['x']} wynosiły {round(dpoint['z'],2)}"


if __name__ == '__main__':
    app.run_server()


