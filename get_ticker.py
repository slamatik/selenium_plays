from dash import Dash, html, dcc, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import datetime as dt
import yfinance as yf

app = Dash(__name__)

ticker_database = {}

holders = pd.read_csv('hold.csv')

candles_config = {
    'modeBarButtonsToAdd': ["drawline", "drawopenpath", "drawclosedpath", "drawcircle", "drawrect", "eraseshape"]}


def candlestick_graph(df):
    fig = go.Figure(data=go.Candlestick(x=df.index, close=df.Close, open=df.Open, high=df.High, low=df.Low))
    fig.update_xaxes(
        rangebreaks=[dict(bounds=['sat', 'mon'])]
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def price_target_graph(df, info):
    pt_date = dt.datetime.today() + dt.timedelta(25)

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


app.layout = html.Div([
    dbc.Row([
        html.Div('Please Enter Ticker: '),
        dcc.Input(id='input', value='', type='text'),
        html.Button(id='button', children='Submit')
    ]),
    dbc.Row([
        dcc.Graph(id='candles', config=candles_config)
        # html.H1(id='ticker')
    ]),
    dbc.Row([
        dbc.Col([
            html.Div('Col 1')
        ]),
        dbc.Col([
            dash_table.DataTable(holders.to_dict('records'), [{'name': i, 'id': i} for i in holders.columns]),
        ]),
        dbc.Col([
            dcc.Graph(id='pt', config={'displayModeBar': False})
        ])
    ], style={'display': 'flex', 'justify': 'center', 'align': 'center'}),
])


@app.callback(
    # Output('ticker', 'children'),
    Output('candles', 'figure'),
    Output('pt', 'figure'),
    Input('button', 'n_clicks'),
    State('input', 'value')
)
def set_ticker(n_clicks, input_value):
    if n_clicks:
        if input_value not in ticker_database:
            ticker = yf.Ticker(input_value)
            ticker_data = ticker.history(period='1y', interval='1d')
            ticker_info = ticker.info
            ticker_database[input_value] = [ticker_data, ticker_info]
        return candlestick_graph(ticker_database[input_value][0]), price_target_graph(ticker_database[input_value][0],
                                                                                      ticker_database[input_value][1])
    else:
        return go.Figure(), go.Figure()
        # return f'Ticker: {ticker_database[input_value]}'


if __name__ == '__main__':
    app.run_server(debug=True)
