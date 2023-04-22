import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from mysql_utils import mysql_get_all_keywords, mysql_year_publication, mysql_add_favorite_faculty, mysql_get_all_favorite_faculties, mysql_delete_favorite_faculty, mysql_add_favorite_publication, mysql_delete_favorite_publication, mysql_get_all_favorite_publication
from neo4j_utils import neo4j_get_all_universties, neo4j_get_professor_university, neo4j_get_university_keywords, neo4j_get_all_faculty
from mongodb_utils import mongodb_topn_publications


neo4j_all_universities = neo4j_get_all_universties()
neo4j_all_faculty = neo4j_get_all_faculty()
all_keywords = mysql_get_all_keywords()
all_favorite_faculties = mysql_get_all_favorite_faculties()
all_favorite_publications = mysql_get_all_favorite_publication()
default_color = 'rgb(121, 41, 82)'

app = Dash(external_stylesheets=[dbc.themes.UNITED])


app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
    
            dbc.Card(dbc.Row(html.H1(children='Academic World: Explore Research Topics', style={'textAlign':'center'})), body=True),
            html.Br(),

            #widget1 using Neo4j
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        html.Div([
                            html.H4(children="Find Universities/Professors with Given Keyword"),
                            dbc.Row([
                                dbc.Col( html.Label(children='Keyword:', style={'textAlign':'right'}), width=1),
                                dbc.Col(
                                    dcc.Dropdown(
                                        options=[k["name"] for k in all_keywords],
                                        value='database systems', id="input1"  
                                    ), width=3
                                ),
                                dbc.Col(dcc.Input(id='num', type='number', value=10, min=1, style={'width':80}))
                            ], align='center'),
                            html.Br(),
                            dash_table.DataTable(
                                columns = [{'name':'Faculty Name','id':'fname'}, {'name':'University Name','id':'uname'}, 
                                        {'name':'# of Publications','id':'n_pubs'}, {'name':'Interest Score','id':'score'}],
                                id='faculty_university_table',
                                fixed_rows={'headers': True},
                                style_table={'overflowY':'auto'},
                                style_data={'height':'auto','minWidth':'140px','width':'140px','maxWidth':'200px',
                                            'color':default_color,'border':'1px solid {}'.format(default_color)},
                                style_cell_conditional=[{'if': {'column_id':'uname'}, 'width':'150%'}],
                                style_header={'backgroundColor':default_color,'color':'white'}
                            )
                        ])
                    ], align="center")
                ])
            ),
            html.Br(),

            #widget2 using mysql 
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        html.Div([
                            html.H4(children="Find # of Publications by Year with Given Keyword"),
                            dbc.Row([
                                dbc.Col(html.Label(children='Keyword:', style={'textAlign':'right'}), width=1),
                                dbc.Col(
                                    dcc.Dropdown(
                                        options=[k["name"] for k in all_keywords],
                                        value='database systems', id="input2"  
                                    ), width=3
                                )
                            ], align='center'),
                            html.Br(),
                            dcc.Graph(id='year_npubs')
                        ])
                    ], align="center")
                ])
            ),
            html.Br(),

            dbc.Row([   
                dbc.Col(
                    #widget3 using mongodb
                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(children="Find Top n Most-Cited Publications with Given Keyword"),
                                dbc.Row([
                                    dbc.Col(html.Label(children='Keyword:', style={'textAlign':'right'}), width='auto'),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            options=[k["name"] for k in all_keywords],
                                            value='database systems', id="input3"  
                                        ), width=6
                                    ),
                                    dbc.Col(dcc.Input(id='num2', type='number', value=10, min=1, style={'width': 80}))
                                ], align='center'),
                                html.Br(),
                                dash_table.DataTable(
                                    columns = [{'name':'Title','id':'title'}, {'name':'Venue','id':'venue'}, 
                                            {'name':'Published Year','id':'year'}, {'name':'# of citations','id':'numCitations'}],
                                    id='numCitations_table',
                                    fixed_rows={'headers': True},
                                    style_table={'overflowX':'auto','overflowY':'auto'},
                                    style_data={'whiteSpace':'normal','height':'auto','minWidth':'180px','width':'180px','maxWidth': '180px',
                                                'color':default_color,'border':'1px solid {}'.format(default_color)},
                                    style_header={'backgroundColor':default_color,'color':'white'}
                                )
                            ])
                        ])
                    ), width=7
                ),

                dbc.Col(
                    #widget4 using Neo4j
                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(children="Find Top n Keywords for Given University"),
                                dbc.Row([
                                    dbc.Col(html.Label(children='University:', style={'textAlign':'right'}), width='auto'),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            options=[k["name"] for k in neo4j_all_universities],
                                            value='University of illinois at Urbana Champaign', id="input4" 
                                        ), width=6
                                    ),
                                    dbc.Col(dcc.Input(id='num3', type='number', value=10, min=1, style={'width':80}))
                                ], align='center'),
                                html.Br(),
                                dcc.Graph(id='keyword_score')
                            ])
                        ])
                    ), width=5
                )
            ], align="center"),
            html.Br(),

            #widget5 using mysql
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(children="Add/Delete Favorite Faculty"),
                                dbc.Row([
                                    dbc.Col(html.Label(children='Name:', style={'textAlign':'right'}), width='auto'),
                                    dbc.Col(dbc.Input(id='input5', value='Your favorite faculty name', type='text'), width=6),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            options=[{'label':'Add','value':'add'}, {'label':'Delete','value':'delete'}],
                                            value='add', id='action'
                                        ), width=2
                                    ),
                                    dbc.Col(dbc.Button(id='submit', n_clicks=0, children='Submit', outline=True, color="dark", className="me-1"), width='auto')
                                ], align='center'),
                                html.Br(),
                                dash_table.DataTable(
                                    columns = [{'name':'Name','id':'Name'}, {'name':'Position','id':'Position'}, 
                                            {'name':'University','id':'University'}, {'name':'Email','id':'Email'}, {'name':'Phone','id':'Phone'}],
                                    id='favorite_faculty_table',
                                    fixed_rows={'headers': True},
                                    style_table={'overflowX':'auto','overflowY':'auto'},
                                    style_data={'whiteSpace':'normal','height':'auto','minWidth':'180px','width':'180px','maxWidth':'180px',
                                                'color':default_color,'border':'1px solid {}'.format(default_color)},
                                    style_header={'backgroundColor':default_color,'color':'white'}
                                )
                            ])
                        ])
                    ), width=6
                ),

                dbc.Col(
                    #widget6 using mysql
                    dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.H4(children="Add/Delete Favorite Publication"),
                                dbc.Row([
                                    dbc.Col(html.Label(children='Name:', style={'textAlign':'right'}), width='auto'),
                                    dbc.Col(dbc.Input(id='input6', value='Your favorite publication name', type='text'), width=6),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            options=[{'label':'Add','value':'add'}, {'label':'Delete','value':'delete'}],
                                            value='add', id='action2'
                                        ), width=2
                                    ),
                                    dbc.Col(dbc.Button(id='submit2', n_clicks=0, children='Submit', outline=True, color="dark", className="me-1"), width='auto')
                                ], align='center'),
                                html.Br(),
                                dash_table.DataTable(
                                    columns = [{'name':'Title','id':'Title'}, {'name':'Author','id':'Author'}, 
                                               {'name':'Year','id':'Year'}, {'name':'Venue','id':'Venue'}],
                                    id='favorite_publication_table',
                                    fixed_rows={'headers': True},
                                    style_table={'overflowX':'auto','overflowY':'auto'},
                                    style_data={'whiteSpace':'normal','height':'auto','minWidth':'180px','width':'180px','maxWidth':'180px',
                                                'color':default_color,'border':'1px solid {}'.format(default_color)},
                                    style_header={'backgroundColor':default_color,'color':'white'}
                                )
                            ])
                        ])
                    ), width=6
                )
            ], align="center"),
            html.Br()
        ]), color='dark'
    )
], className="pad-row")



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
    fig.update_traces(line_color=default_color)
    return fig

#widget3
@callback(
    Output('numCitations_table', 'data'),
    Input('input3', 'value'),
    Input('num2','value'),
)
def update_numCitations(input_keyword, n_result):
    if not input_keyword:
        return dash.no_update
    result = mongodb_topn_publications(input_keyword, n_result)
    return result

#widget4
@callback(
    Output('keyword_score', 'figure'),
    Input('input4', 'value'),
    Input('num3', 'value'),
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
    fig = px.pie(df,values="total_score",  names="name", template="seaborn")
    return fig

#widget5
@callback(
    Output('favorite_faculty_table', 'data'),
    State('input5', 'value'),
    State('action', 'value'),
    Input('submit', 'n_clicks')
)
def add_favorite_faculty(input_faculty, action, n_clicks):
    result = all_favorite_faculties
    if action == "add" and n_clicks > 0:
        result = mysql_add_favorite_faculty(input_faculty)
    elif action == "delete" and n_clicks > 0:
        result = mysql_delete_favorite_faculty(input_faculty)
    return result

#widget6
@callback(
    Output('favorite_publication_table', 'data'),
    State('input6', 'value'),
    State('action2', 'value'),
    Input('submit2', 'n_clicks')
)
def add_favorite_publication(input_publication, action, n_clicks):
    result = all_favorite_publications
    if action == "add" and n_clicks > 0:
        result = mysql_add_favorite_publication(input_publication)
    elif action == "delete" and n_clicks > 0:
        result = mysql_delete_favorite_publication(input_publication)
    return result

if __name__ == '__main__':
    app.run_server()