# scatterplot with two DropDown boxes for the different indicators
# a slide for the different years in the data
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Data cleaning
df = pd.read_csv('nama_10_gdp_1_Data.csv')
df['Value'].replace({':': np.nan}, inplace=True)
df.dropna(inplace=True)
df_index_100 = df[df['UNIT'] == 'Chain linked volumes, index 2010=100']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = df['NA_ITEM'].unique()
available2 = df['GEO'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i}
                         for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i}
                         for i in available_indicators],
                value='Value added, gross'
            )
        ],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
 
    dcc.Graph(id='indicator-graphic'),
    dcc.Graph(id='indicator-graphic2'),


    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        marks={str(year): str(year) for year in df['TIME'].unique()},
        step=None
    )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, year_value):
    dff = df[df['TIME'] == year_value]

    return {
        'data': [dict(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)