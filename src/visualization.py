import pandas as pd
import plotly.graph_objects as go 

import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

#Dataframe determined from running the cleaning script on the raw election odds
df = pd.read_csv('data/final_odds.csv', parse_dates=['date'])

app.layout = html.Div([
    html.H1('2020 Presidential Election Forecast', style = {'text-align': 'center'}),
    html.H2('Derived from Betting Markets', style = {'text-align': 'center'}),

    dcc.Dropdown(id = 'select_timeframe',
    options = [
        {'label': 'All', 'value' : 'All'},
        {'label': 'Before First Results', 'value' : 'Before'},
        {'label': 'After First Results', 'value' : 'After'},
        {'label': 'Election Night', 'value': 'Election Night'}],
        multi = False,
        value = 'All',
        style = {'width': '40%'}
    ),
        
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='election_odds', figure = {}),

    html.Br(),
    html.Br(),
    html.H1('Sources'),
    html.Div([
        html.P([
            html.A(
                '[1]',
                href = 'https://www.sportsbettingdime.com/politics/2020-us-presidential-election-odds/', 
             ),
            ': Betting Market odds for each candidate leading up to Election Night',
        ]),
        html.P([
            html.A(
                '[2]',
                href = 'https://www.gamblingsites.org/blog/2020-election-betting-odds-election-night-changes/', 
             ),
            ': More Precise hourly Odds on Election Night',
        ]),
        html.P([
            html.A(
                '[3]',
                href = 'https://blog.ap.org/behind-the-news/calling-the-2020-presidential-race-state-by-state', 
             ),
            ': Associated Press Election Timeline',
        ]),
        html.P([
            html.A(
                '[4]',
                href = 'https://www.nytimes.com/interactive/2020/07/03/us/george-floyd-protests-crowd-size.html', 
             ),
            ': Black Lives Matter protest data',
        ]),
        html.P([
            html.A(
                '[5]',
                href = 'https://covid.cdc.gov/covid-data-tracker/#trends_totalandratedeaths', 
             ),
            ': COVID-19 data',
        ]),
        html.P([
            html.A(
                '[6]',
                href = 'https://en.wikipedia.org/wiki/Timeline_of_the_2020_United_States_presidential_election_(January-October_2020)', 
             ),
            ': 2020 Campaign Timeline',
        ]),
        html.P([
            html.A(
                '[7]',
                href = 'https://www.nytimes.com/interactive/2020/us/politics/polls-close.html', 
             ),
            ': Election Night poll closing information',
        ]),
        html.P([
            html.A(
                '[8]',
                href = 'https://www.cnbc.com/2020/11/04/election-live-results-updates-trump-biden.html', 
             ),
            ': WI and MI Election results',
        ]),
    ]),
])

@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
     Output(component_id='election_odds', component_property = 'figure')],
    [Input(component_id = 'select_timeframe', component_property='value')]
)

def update_graph(chosen_option):
    container = 'Chosen Timeframe: {0}'.format(chosen_option)

    time_map = {
        'Before': True,
        'After': False,
        'Election Night': False
    }

    display_df = df[df['pre_first_results']==time_map[chosen_option]] if chosen_option in time_map.keys() else df.copy()

    if chosen_option == 'Election Night':
        display_df = display_df[display_df.date<=pd.Timestamp(2020,11,4,10)]

    display_df_markers = display_df[display_df['notes'].notnull()]

    fig={
        "data": [
            go.Scatter(
                x=display_df['date'],
                y=display_df['trump_win_perc'],
                # hovertext=display_df['notes'],
                line={"color": "#ff4a43"},
                mode="lines",
                name="Trump Win %",
                legendgroup='Trump',
            ),
            go.Scatter(
                x=display_df['date'],
                y=display_df['biden_win_perc'],
                # hovertext=display_df['notes'],
                line={"color": "#196afe"},
                mode="lines",
                name="Biden Win %",
            ),
            go.Scatter(
                x=display_df_markers['date'],
                y=[0]*len(display_df_markers),
                text=display_df_markers['notes'],
                marker=dict(
                    color='goldenrod',
                    symbol='star',
                    size=10,
                    line=dict(
                        color='MediumPurple',
                        # width=2
                    ),
                ),
                hoverinfo='x+text',
                mode="markers",
                name="Key Events",
                # legendgroup='Trump'
            ),
        ],
        'layout': {
            'title' : 'Candidate Win Percentage Over Time',
            'title_x': 0.5,
            'xaxis': {
                'title': {
                    'text': 'Date'
                },
                'range' :[
                    display_df['date'].min(),
                    display_df['date'].max()
                ]
            },
            'yaxis': {
                'title': 'Win Percentage',
                 'range' :[
                    -5,
                    100
                ]
            }
            # 'hovermode' = 'x unified'
        }
    }

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)
