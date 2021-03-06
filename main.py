from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import datetime as dt
import yfinance as yf

# PRICE TARGET GRAPH
ticker = yf.Ticker('PLTR')
df = ticker.history(period='1y', interval='1d')
pt_date = dt.datetime.today() + dt.timedelta(25)
info = ticker.info

target_high = info['targetHighPrice']
target_mean = info['targetMeanPrice']
target_meadian = info['targetMedianPrice']
target_low = info['targetLowPrice']

pt_dates = [df.index[-1]] + [pt_date]
pt_high = [df.Close[-1]] + [target_high]
pt_mean = [df.Close[-1]] + [target_mean]
pt_low = [df.Close[-1]] + [target_low]

year_high = [df.Close.max()] * 2
year_high_dates = [df.index[0]] + [df.Close.idxmax()]

year_low = [df.Close.min()] * 2
year_low_dates = [df.index[0]] + [df.Close.idxmin()]


def candlestick_graph():
    fig = go.Figure(data=go.Candlestick(x=df.index, close=df.Close, open=df.Open, high=df.High, low=df.Low))
    fig.update_xaxes(
        rangebreaks=[dict(bounds=['sat', 'mon'])]
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def price_target_graph():
    # fig = go.Figure()
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    hovertemplate = """
    Date: %{x}<br>
    Close price: %{y}
    <extra></extra>
    """

    fig.add_trace(go.Scatter(x=df.index, y=df.Close, name='Close price', hovertemplate=hovertemplate), secondary_y=True)

    fig.add_trace(
        go.Scatter(legendgroup='price-target', legendgrouptitle_text='1 Year Price Target', x=pt_dates, y=pt_high,
                   name='High PT', line=dict(dash='dot')), secondary_y=True)
    fig.add_trace(go.Scatter(legendgroup='price-target', x=pt_dates, y=pt_mean, name='Mean PT', line=dict(dash='dot')),
                  secondary_y=True)
    fig.add_trace(go.Scatter(legendgroup='price-target', x=pt_dates, y=pt_low, name='Low PT', line=dict(dash='dot')),
                  secondary_y=True)

    fig.add_trace(
        go.Scatter(legendgroup='high_low', legendgrouptitle_text='1 Year High and Low', x=year_high_dates, y=year_high,
                   mode='lines', line=dict(dash='dot'), name='High'), secondary_y=True)
    fig.add_trace(go.Scatter(legendgroup='high_low', x=year_low_dates, y=year_low, mode='lines', line=dict(dash='dot'),
                             name='Low'), secondary_y=True)

    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            tickmode='array',
            tickvals=df.index[4::30].to_list() + [pd.Timestamp(pt_dates[-1])],
            ticktext=[d.strftime('%b-%y') for d in df.index[4::30]] + ['1 Year'],
            showgrid=False),
        yaxis=dict(
            showgrid=False,
        ),
        yaxis2=dict(
            showgrid=False,
        )
    )
    return fig


app = Dash(__name__)

app.layout = html.Div([
    dbc.Row([
        html.Div('Please Enter Ticker: '),
        dcc.Input(id='ticker-input'),
        html.Button(id='submit-ticker-button', children='Submit')
    ]),
    dbc.Row([
        dcc.Graph('candles')
    ]),
    dbc.Row([
        dcc.Checklist(id='ta', options=['50 Day Simple Moving Average', '9 Day Simple Moving Average'], inline=True)
    ]),
])


@app.callback(
    Output('candles', 'figure'),
    Input('ta', 'value')
)
def update_chart(value):
    data = {'200 Day Simple Moving Average': 200,
            '50 Day Simple Moving Average': 50,
            '9 Day Simple Moving Average': 9,
            'Bollinger Bands': 'asd'}
    if value:
        fig = candlestick_graph()
        if len(value) == 1:
            window = data[value[0]]
            ma_values = df.Close.rolling(window).mean()
            fig.add_trace(go.Scatter(x=df.index, y=ma_values, name=value[0], line=dict(color='royalblue')))
        else:
            for tool in value:
                window = data[tool]
                ma_values = df.Close.rolling(window).mean()
                fig.add_trace(go.Scatter(x=df.index, y=ma_values, name=tool, line=dict(color='#00D')))
    else:
        fig = go.Figure()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


import trendln