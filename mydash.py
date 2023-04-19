import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from mysql_utils import mysql_get_all_keywords, mysql_year_publication, mysql_add_favorite_faculty, mysql_get_all_favorite_faculties, mysql_delete_favorite_faculty
from neo4j_utils import neo4j_get_all_universties, neo4j_get_professor_university, neo4j_get_university_keywords, neo4j_get_all_faculty
from mongodb_utils import mongodb_top10_publications


neo4j_all_universities = neo4j_get_all_universties()
neo4j_all_faculty = neo4j_get_all_faculty()
all_keywords = mysql_get_all_keywords()
all_favorite_faculties = mysql_get_all_favorite_faculties()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    #widget1 using Neo4j
    html.H1(children='CS411 Project', style={'textAlign':'center'}),
    html.Div([
        html.H6(children="Find Universities/Professors with given Keyword"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Keyword:', style={'textAlign':'right'})
                ,width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["name"] for k in all_keywords],
                    value='database systems',
                    id="input1"  
                ),
            ),
            dbc.Col(dcc.Input(id='num', type='number', value=10)),
        ]),
        html.Br(),
        dash_table.DataTable(
            columns = [{'name': 'Faculty Name', 'id': 'fname'}, {'name': 'University Name', 'id': 'uname'}, 
                    {'name': '# of Publications', 'id': 'n_pubs'}, {'name': 'Interest Score', 'id': 'score'}],
            id='faculty_university_table'
        )
    ]),

    #widget2 using mysql 
    html.Div([
        html.H6(children="FInd # of Publications by Year with given Keyword"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Keyword:', style={'textAlign':'right'})
                ,width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["name"] for k in all_keywords],
                    value='database systems',
                    id="input2"  
                ),
            ),
        ]),
        html.Br(),
        dcc.Graph(id='year_npubs')
    ]),

    #widget3 using mongodb
    html.Div([
        html.H6(children="Find Top10 publications by NumCiations with given Keyword"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Keyword:', style={'textAlign':'right'})
                ,width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["name"] for k in all_keywords],
                    value='database systems',
                    id="input3"  
                ),
            ),
            #dbc.Col(dcc.Input(id='num', type='number', value=10)),
            #dbc.Col(html.Button('Search', id='search_button')),
        ]),
        html.Br(),
        dash_table.DataTable(
            columns = [{'name': 'Title', 'id': 'title'}, {'name': 'Venue', 'id': 'venue'}, 
                    {'name': 'Published Year', 'id': 'year'}, {'name': '# of citations', 'id': 'numCitations'}],
            id='numCitations_table',
            style_cell={'textAlign': 'left'},
        )
    ]),

    #widget4 using Neo4j
    html.Div([
        html.H6(children="Find Top n Keywords for the given University"),
        dbc.Row([
            dbc.Col(
                html.Label(children='University:', style={'textAlign':'right'}),width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["name"] for k in neo4j_all_universities],
                    value='University of illinois at Urbana Champaign',
                    id="input4" 
                )
            ),
            dbc.Col(dcc.Input(id='num2', type='number', value=10)),
        ]),
        html.Br(),
        dcc.Graph(id='keyword_score')
    ]),

    #widget5 using mysql
    html.Div([
        html.H6(children="Add/Delete Favorite Faculty"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Faculty Name:', style={'textAlign':'right'}),width=2),
            dbc.Col(
                dcc.Input(id='input5', value='your favorite faculty name', type='text')
                ),
            dbc.Col(
                dcc.Dropdown(
                    options=[
                        {'label': 'Add', 'value': 'add'},
                        {'label': 'Delete', 'value': 'delete'},
                    ],
                    value='add',
                    id = 'action'
                ),
            ),
            dbc.Col(
                html.Button(id='submit', n_clicks=0, children='Submit'),
            )
        ]),
        html.Br(),
        dash_table.DataTable(
            columns = [{'name': 'Name', 'id': 'Name'}, {'name': 'Position', 'id': 'Position'}, 
                    {'name': 'University', 'id': 'University'}, {'name': 'Email', 'id': 'Email'}, {'name': 'Phone', 'id': 'Phone'}],
            id='favorite_faculty_table',
            data = all_favorite_faculties,
            style_cell={'textAlign': 'left'}
        )
    ]),
])

#widget1
@callback(
    Output('faculty_university_table', 'data'),
    Input('input1', 'value'),
    Input('num', 'value'),
)
def update_table(input_keyword, n_result):
    if not input_keyword:
        return dash.no_update
    result = neo4j_get_professor_university(input_keyword,n_result)
    return result

#widget2
@callback(
    Output('year_npubs', 'figure'),
    Input('input2', 'value')
)
def update_graph(input_keyword):
    if not input_keyword:
        return dash.no_update
    result = mysql_year_publication(input_keyword)
    data = {"year": [], "n_pubs": []}
    for record in result:
        data["year"].append(record["year"])
        data["n_pubs"].append(record["n_pubs"])
    df = pd.DataFrame(data)
    fig = px.bar(df,x="year", y="n_pubs")
    return fig

#widget3
@callback(
    Output('numCitations_table', 'data'),
    Input('input3', 'value'),
)
def update_numCitations(input_keyword):
    if not input_keyword:
        return dash.no_update
    result = mongodb_top10_publications(input_keyword)
    return result

#widget4
@callback(
    Output('keyword_score', 'figure'),
    Input('input4', 'value'),
    Input('num2', 'value'),
)
def update_graph2(input_university, n_result):
    if not input_university:
        return dash.no_update
    result = neo4j_get_university_keywords(input_university, n_result)
    data = {"name": [], "total_score": []}
    for record in result:
        data["name"].append(record["name"])
        data["total_score"].append(record["total_score"])
    df = pd.DataFrame(data)
    fig = px.pie(df,values="total_score",  names="name")
    return fig

#widget5
@callback(
    Output('favorite_faculty_table', 'data'),
    State('input5', 'value'),
    State('action', 'value'),
    Input('submit', 'n_clicks')
)
def add_favorite_faculty(input_faculty, action, n_clicks):
    if action == "add" and n_clicks > 0:
        result = mysql_add_favorite_faculty(input_faculty)
    elif action == "delete" and n_clicks > 0:
        result = mysql_delete_favorite_faculty(input_faculty)
    return result

if __name__ == '__main__':
    app.run_server()
