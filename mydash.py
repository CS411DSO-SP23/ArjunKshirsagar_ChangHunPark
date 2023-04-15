import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc

from mysql_utils import mysql_get_all_keywords, mysql_get_professor_university
from neo4j_utils import neo4j_get_all_keywords, neo4j_get_professor_university

all_keywords = neo4j_get_all_keywords()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    html.H1(children='CS411 Project', style={'textAlign':'center'}),
    html.Div([
        html.H6(children="Find universities/professors with keywords"),
        dbc.Row([
            dbc.Col([
                html.Label(children='Keyword:', style={'textAlign':'right'})
                ],width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["name"] for k in all_keywords],
                    placeholder='Select your keyword...',
                    id="input"  
                ),
            ),
            dbc.Col(dcc.Input(id='num', type='number', value=10)),
            dbc.Col(html.Button('Search', id='search_button')),
        ]),
        html.Br(),
        dash_table.DataTable(
            columns = [{'name': 'Faculty Name', 'id': 'fname'}, {'name': 'University Name', 'id': 'uname'}, 
                    {'name': '# of Publications', 'id': 'n_pubs'}, {'name': 'Interest Score', 'id': 'score'}],
            id='faculty_university_table'
        )
    ]),
    html.Div([
        html.Div(dcc.Input(type='text')),
        html.Button('Submit'),
    ]),
    html.Div([
        html.Div(dcc.Input(type='text')),
        html.Button('Submit'),
    ]),
    html.Div([
        html.Div(dcc.Input(type='text')),
        html.Button('Submit'),
    ]),
    html.Div([
        html.Div(dcc.Input(type='text')),
        html.Button('Submit'),
    ]),
    html.Div([
        html.Div(dcc.Input(type='text')),
        html.Button('Submit'),
    ]),
])

@callback(
    Output('faculty_university_table', 'data'),
    State('input', 'value'),
    State('num', 'value'),
    Input('search_button', 'n_clicks')
)
def update_table(input_keyword, n_result, n_clicks):
    if not input_keyword:
        return dash.no_update
    result = neo4j_get_professor_university(input_keyword,n_result)
    return result

if __name__ == '__main__':
    app.run_server()