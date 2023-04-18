import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from mysql_utils import mysql_get_all_keywords, mysql_year_publication, mysql_create_favorite_faculty, mysql_update_favorite_faculty, mysql_create_favorite_universities, mysql_update_favorite_universities
from neo4j_utils import neo4j_get_all_keywords, neo4j_get_all_universties, neo4j_get_all_faculty, neo4j_get_professor_university, neo4j_get_university_keywords
from mongodb_utils import mongodb_get_all_keywords, mongodb_top10_publications


neo4j_all_keywords = neo4j_get_all_keywords()
neo4j_all_universities = neo4j_get_all_universties()
neo4j_all_faculty = neo4j_get_all_faculty()
mysql_all_keywords = mysql_get_all_keywords()
mongodb_all_keywords = mongodb_get_all_keywords()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    #widget1
    html.H1(children='CS411 Project', style={'textAlign':'center'}),
    html.Div([
        html.H6(children="Find Faculty with given Keyword"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Keyword:', style={'textAlign':'right'}), width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["name"] for k in neo4j_all_keywords],
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
    #widget2
    html.Div([
        html.H6(children="Find # of Publications by Year with given Keyword"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Keyword:', style={'textAlign':'right'}), width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["name"] for k in mysql_all_keywords],
                    value='database systems',
                    id="input2"  
                ),
            ),
        ]),
        html.Br(),
        dcc.Graph(id='year_npubs')
    ]),
    #widget3
    html.Div([
        html.H6(children="Find Top 10 Most-Cited Publications with given Keyword"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Keyword:', style={'textAlign':'right'}), width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[k["_id"] for k in mongodb_all_keywords],
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
    #widget4
    html.Div([
        html.H6(children="Find Top n Keywords for given University"),
        dbc.Row([
            dbc.Col(
                html.Label(children='University:', style={'textAlign':'right'}), width=1),
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
    #widget5
    html.Div([
        html.H6(children="Add/Remove Favorite Faculty"),
        dbc.Row([
            dbc.Col(
                html.Label(children='Faculty Name:', style={'textAlign':'right'}), width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[f["name"] for f in neo4j_all_faculty],
                    value='Agouris,Peggy',
                    id="input5"  
                ),
            ),
            dbc.Col(
                dcc.Dropdown(options=['Add','Remove'], value='Add', id="action1"),
            )
        ]),
        html.Button('Enter', id='enter_value_1', n_clicks=0),
        html.Br(),
        dash_table.DataTable(
            columns = [{'name': 'Name', 'id': 'fname'}, {'name': 'Position', 'id': 'position'}, 
                    {'name': 'University', 'id': 'uname'}, {'name': 'Email', 'id': 'email'}, {'name': 'Phone', 'id': 'phone'}],
            id='favorite_faculty_table',
            style_cell={'textAlign': 'left'}
        )
    ]),
    #widget6
    html.Div([
        html.H6(children="Add/Remove Favorite University"),
        dbc.Row([
            dbc.Col(
                html.Label(children='University Name:', style={'textAlign':'right'}), width=1),
            dbc.Col(
                dcc.Dropdown(
                    options=[u["name"] for u in neo4j_all_universities],
                    value='University of illinois at Urbana Champaign',
                    id="input6"  
                ),
            ),
            dbc.Col(
                dcc.Dropdown(options=['Add','Remove'], value='Add', id="action2"),
            )
        ]),
        html.Button('Enter', id='enter_value_2', n_clicks=0),
        html.Br(),
        dash_table.DataTable(
            columns = [{'name': 'Name', 'id': 'name'}],
            id='favorite_university_table',
            style_cell={'textAlign': 'left'}
        )
    ])
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
    fig = px.line(df, x="year", y="n_pubs", labels=dict(year='Year', n_pubs='# of Publications'))
    fig.update_xaxes(tickangle = 45, title_text = 'Year')
    fig.update_yaxes(title_text = '# of Publications')
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
    fig = px.pie(df, values="total_score",  names="name")
    return fig

#widget5
@callback(
    Output('favorite_faculty_table', 'data'),
    State('input5', 'value'),
    State('action1', 'value'),
    Input('enter_value_1', 'n_clicks'),
)
def update_fav_faculty(input_faculty, action, n_clicks):
    if not input_faculty:
        return dash.no_update
    if n_clicks == 1 and action=='Remove':
        return 'Cannot remove from empty table.'
    if n_clicks == 1 and action=='Add':
        result = mysql_create_favorite_faculty(input_faculty, action)
    else:
        result = mysql_update_favorite_faculty(input_faculty, action)
    return result
    
#widget6
@callback(
    Output('favorite_university_table', 'data'),
    State('input6', 'value'),
    State('action2', 'value'),
    Input('enter_value_2', 'n_clicks'),
)
def update_fav_universities(input_university, action, n_clicks):
    if not input_university:
        return dash.no_update
    if n_clicks == 1 and action=='Remove':
        return 'Cannot remove from empty table.'
    if n_clicks == 1 and action=='Add':
        result = mysql_create_favorite_universities(input_university, action)
    else:
        result = mysql_update_favorite_universities(input_university, action)
    return result


if __name__ == '__main__':
    app.run_server()