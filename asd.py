import numpy as np
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
df_table = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
df_scatter = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
df_slider = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


colors = {'background': '#111111', 'text': '#7FDBFF'}

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        'Input: ',
        dcc.Input(id='input-number', value='0', type='text')
    ]),
    html.Div([
        dcc.Graph(id='graph-x2'),
        dcc.Graph(id='graph-x3')
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Div([
        dcc.Graph(id='graph-x4'),
        dcc.Graph(id='graph-x5')
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Div([
        dcc.Graph(id='graph-x6'),
        dcc.Graph(id='graph-x7')
    ], style={'display': 'flex', 'flex-direction': 'row'})
])


@app.callback(
    Output(component_id='graph-x2', component_property='figure'),
    Output(component_id='graph-x3', component_property='figure'),
    Output(component_id='graph-x4', component_property='figure'),
    Output(component_id='graph-x5', component_property='figure'),
    Output(component_id='graph-x6', component_property='figure'),
    Output(component_id='graph-x7', component_property='figure'),
    Input(component_id='input-number', component_property='value')
)
def update_figure(input_value):
    x = np.arange(-int(input_value), int(input_value) + 1)
    y_2 = np.array([i ** 2 for i in x])
    y_3 = np.array([i ** 3 for i in x])
    y_4 = np.array([i ** 4 for i in x])
    y_5 = np.array([i ** 5 for i in x])
    y_6 = np.array([np.sin(i/4) for i in x])
    y_7 = np.array([np.cos(i/4) for i in x])

    fig1 = px.line(x=x, y=y_2)
    fig2 = px.line(x=x, y=y_3)
    fig3 = px.line(x=x, y=y_4)
    fig4 = px.line(x=x, y=y_5)
    fig5 = px.line(x=x, y=y_6)
    fig6 = px.line(x=x, y=y_7)

    return fig1, fig2, fig3, fig4, fig5, fig6


if __name__ == '__main__':
    app.run_server(debug=True)
