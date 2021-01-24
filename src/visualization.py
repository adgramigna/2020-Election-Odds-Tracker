import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 

import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv('data/final_odds.csv', parse_dates=['date'])
# df_all = df.copy()

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

@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
     Output(component_id='election_odds', component_property = 'figure')],
    [Input(component_id = 'select_timeframe', component_property='value')]
)

def update_graph(chosen_option):
    print(chosen_option, type(chosen_option))

    container = 'Chosen Timeframe: {0}'.format(chosen_option)

    time_map = {
        'Before': True,
        'After': False
    }

    display_df = df[df['pre_first_results']==time_map[chosen_option]] if chosen_option in time_map.keys() else df.copy()

    print(display_df)

    html.H6("Title", className="subtitle padded"),
    
    graph = dcc.Graph(
        id="graph-4",
        figure={
            "data": [
                go.Scatter(
                    x=display_df['date'],
                    y=display_df['trump_win_perc'],
                    hovertext=df['trump_odds'],
                    line={"color": "#ff4a43"},
                    mode="lines+markers",
                    name="Trump Win %",
                ),
                go.Scatter(
                    x=display_df['date'],
                    y=display_df['biden_win_perc'],
                    hovertext=df['biden_odds'],
                    line={"color": "#196afe"},
                    mode="lines+markers",
                    name="Biden Win %",
                ),
            ]
        }
    ) 

    return container, graph.figure

if __name__ == '__main__':
    app.run_server(debug=True)
