from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import datetime as dt
import yfinance as yf

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def candlestick_graph(df=None):
    if df is not None:
        fig = go.Figure(data=go.Candlestick(x=df.index, close=df.Close, open=df.Open, high=df.High, low=df.Low))
        fig.update_xaxes(
            rangebreaks=[dict(bounds=['sat', 'mon'])]
        )
    else:
        fig = go.Figure()

    fig.update_layout(xaxis_rangeslider_visible=False, xaxis={'showgrid': False}, paper_bgcolor='LightSteelBlue',
                      margin=dict(l=0, r=5, t=5, b=0))
    return fig

def price_target_graph(df=None, info=None):
    if df is not None:
        pt_date = dt.datetime.today() + dt.timedelta(25)

        target_high = info['targetHighPrice']
        target_mean = info['targetMeanPrice']
        target_median = info['targetMedianPrice']
        target_low = info['targetLowPrice']

        pt_dates = [df.index[-1]] + [pt_date]
        pt_high = [df.Close[-1]] + [target_high]
        pt_mean = [df.Close[-1]] + [target_mean]
        pt_low = [df.Close[-1]] + [target_low]

        year_high = [df.Close.max()] * 2
        year_high_dates = [df.index[0]] + [df.Close.idxmax()]

        year_low = [df.Close.min()] * 2
        year_low_dates = [df.index[0]] + [df.Close.idxmin()]

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
            yaxis=dict(showgrid=False),
            yaxis2=dict(showgrid=False), margin=dict(l=0, r=0, t=0, b=0)
        )
    else:
        fig = make_subplots(specs=[[{'secondary_y': True}]])
        fig.update_layout(
            showlegend=False,
            xaxis=dict(
                tickmode='array',
                showgrid=False),
            yaxis=dict(showgrid=False),
            yaxis2=dict(showgrid=False), paper_bgcolor='lightSteelBlue',
            margin=dict(l=0, r=0, t=0, b=0))
    return fig


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(id='left-columns', width=1, children=[
            dbc.Input(id='input', value='', type='text'),
            html.Button(id='button', children='Submit'),
            dbc.Checklist(options=[
                {"label": "Option 1", "value": 1},
                {"label": "Option 2", "value": 2},
                {"label": "Disabled Option", "value": 3, "disabled": True},
            ])
        ]),
        dbc.Col(id='main-column', children=[
            dcc.RadioItems([' 1D', ' 5D', ' 1M', '6M', 'YTD', '1Y', '5Y', 'Max'], '1D', inputStyle={'margin-left': '20px'}),
            dcc.Graph(id='main-graph')
        ]),
        dbc.Col(id='right-column', width=3, children=[dcc.Graph(id='secondary-graph')])
    ])
])


@app.callback(
    Output('main-graph', 'figure'),
    Output('secondary-graph', 'figure'),
    Input('button', 'n_clicks'),
    State('input', 'value')
)
def set_ticker(n_clicks, input_value):
    if n_clicks:
        ticker = yf.Ticker(input_value)
        ticker_data = ticker.history(period='1y', interval='1d')
        ticker_info = ticker.info
        return candlestick_graph(ticker_data), price_target_graph(ticker_data, ticker_info)
    else:
        return candlestick_graph(), price_target_graph()

if __name__ == '__main__':
    app.run_server(debug=True)