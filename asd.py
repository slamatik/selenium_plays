import numpy as np
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

df_1min = yf.Ticker('AAPL').history(period='5d', interval='1m')
df_2min = yf.Ticker('AAPL').history(period='1mo', interval='2m')
df_5min = yf.Ticker('AAPL').history(period='1mo', interval='5m')

fig_1min = go.Figure(data=[go.Candlestick(x=df_1min.index, open=df_1min.Open, close=df_1min.Close, high=df_1min.High, low=df_1min.Low)])
fig_1min.update_layout()
fig_2min = go.Figure(data=[go.Candlestick(x=df_2min.index, open=df_2min.Open, close=df_2min.Close, high=df_2min.High, low=df_2min.Low)])

figures = {'1 minute': fig_1min,
           '2 minutes': fig_2min,
}

colors = {'background': '#111111', 'text': '#7FDBFF'}

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        'Time Frame: ',
        dcc.RadioItems(['1 minute', '2 minutes', '5 minutes'], '1 minute', id='first-input'),
        dcc.Graph(figure=fig_1min, id='first-figure')
    ])
])

@app.callback(
    Output(component_id='first-figure', component_property='figure'),
    Input(component_id='first-input', component_property='value')
)
def update_first_figure(input_value):
    return figures[input_value]
#
# @app.callback(
#     Output(component_id='graph-x2', component_property='figure'),
#     Output(component_id='graph-x3', component_property='figure'),
#     Output(component_id='graph-x4', component_property='figure'),
#     Output(component_id='graph-x5', component_property='figure'),
#     Output(component_id='graph-x6', component_property='figure'),
#     Output(component_id='graph-x7', component_property='figure'),
#     Input(component_id='input-number', component_property='value')
# )
# def update_figure(input_value):
#     x = np.arange(-int(input_value), int(input_value) + 1)
#     y_2 = np.array([i ** 2 for i in x])
#     y_3 = np.array([i ** 3 for i in x])
#     y_4 = np.array([i ** 4 for i in x])
#     y_5 = np.array([i ** 5 for i in x])
#     y_6 = np.array([np.sin(i/4) for i in x])
#     y_7 = np.array([np.cos(i/4) for i in x])
#
#     fig1 = px.line(x=x, y=y_2)
#     fig2 = px.line(x=x, y=y_3)
#     fig3 = px.line(x=x, y=y_4)
#     fig4 = px.line(x=x, y=y_5)
#     fig5 = px.line(x=x, y=y_6)
#     fig6 = px.line(x=x, y=y_7)
#
#     return fig1, fig2, fig3, fig4, fig5, fig6


if __name__ == '__main__':
    app.run_server(debug=True)
