import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 

import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('data/final_odds.csv', parse_dates=['date'])
df_all = df.copy()

# print(df.head(), df.dtypes)

app.layout = html.Div([
    html.H1('2020 Presidential Election Forecast', style = {'text-align': 'center'}),
    html.H2('Derived from Betting Markets', style = {'text-align': 'center'}),

    dcc.Dropdown(id = 'select_timeframe',
    options = [
        {'label': 'All', 'value' : 'All'},
        {'label': 'Before First Results', 'value' : 'Before'},
        {'label': 'After First Results', 'value' : 'After'}],
        multi = False,
        value = 'All',
        style = {'width': '40%'}
    ),
        
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='election_odds', figure = {})
])

# @app.callback(
#     [Output(component_id = 'output_container', component_property = 'children'),
#      Output(component_id='election_odds', component_property = 'figure')],
#     [Input(component_id = 'select_timeframe', component_property=value)]
# )

if __name__ == '__main__':
    app.run_server(debug=True)
