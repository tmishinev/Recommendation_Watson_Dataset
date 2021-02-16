import pandas as pd
import plotly.express as px  # (version 4.7.0)
import dash_table
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pickle
import plotly
from plotly.graph_objs import Bar
from  flask_caching import Cache
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from custom import load_data
from user_user import get_top_sorted_users, user_user_recs_part2, create_user_item_matrix, get_user_articles
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.LUX])

server = app.server


#paper color const
BGCOLOR = "rgb(245, 245, 245)"
USER_TEMP = 1


df, df_content = load_data()
user_item = create_user_item_matrix(df)


def return_user_articles(USER_TEMP, df, user_item):
    article_id, title = get_user_articles(USER_TEMP, df, user_item)
    df_articles = pd.DataFrame({'article_id' : map(str, article_id), 'title' : title })
    return df_articles

def unique_values_bar(df):
    fig = px.bar(x = df_content.nunique().index, y = df_content.nunique(),  height=400)
    
    fig.update_layout(

        xaxis_title="Content dataframe fields",
        yaxis_title="Unique values",

        )

    fig.update_layout(plot_bgcolor = BGCOLOR, paper_bgcolor = BGCOLOR)

    return fig

def user_int_hist(df):
    
    fig = px.histogram(x = df.groupby('user_id').count()['article_id'],  height=400)

    fig.update_layout(
        xaxis_title="User Interaction Number",
        yaxis_title="Number of Users"
        )

    fig.update_layout(plot_bgcolor = BGCOLOR, paper_bgcolor = BGCOLOR)

    return fig

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(children=[

    dbc.Row(dbc.Col([
                    html.Hr(),
                    html.H3( "Recommendations with IBM Watson ", style={'text-align': 'center', 'size' : 10}),
                    html.Hr()
                    ], width = {'size': 6, 'offset': 3 }
                    ),
            ),
    dbc.Row(
        dbc.Col(dbc.Tabs(id='tabs-example',  children=[
            dbc.Tab(label='Explore Dataset', children = [
                            dbc.Row([
                                    
                                        dbc.Col([   html.Hr(),
                                                    html.H5( "First 5 rows of the User-interaction Dataset", style={'text-align': 'left'}),
                                                    html.Hr(),
                                                    dash_table.DataTable(
                                                        style_cell={
                                                                        'overflow': 'hidden',
                                                                        'textOverflow': 'ellipsis',
                                                                        'maxWidth': 0
                                                                    },
                                                        id='table_df',
                                                        columns=[{"name": i, "id": i} for i in df.columns],
                                                        data=df.head(5).to_dict('records'),
                                                    )], width = {'size': 4, 'offset': 1 }), 

                                        dbc.Col([   html.Hr(),
                                                    html.H5( "First 5 rows in the Content Dataset", style={'text-align': 'left'}),
                                                    html.Hr(),
                                                    dash_table.DataTable(
                                                        style_cell={
                                                                        'overflow': 'hidden',
                                                                        'textOverflow': 'ellipsis',
                                                                        'maxWidth': 0
                                                                    },
                                                        id='table_content',
                                                        columns=[{"name": i, "id": i} for i in df_content.columns],
                                                        data=df_content.head(5).to_dict('records'),
                                                    )], width = {'size': 4, 'offset': 1 })          

                                    ]),

                            dbc.Row([dbc.Col([

                                                html.Hr(),
                                                dcc.Graph(id='bar_unique_values', figure=user_int_hist(df)),

                                            ], width = {'size': 4, 'offset': 1 }
                                            ),

                                    dbc.Col([

                                                 html.Hr(),
                                                dcc.Graph(id='bar_hist', figure=unique_values_bar(df)),

                                            ], width = {'size': 4, 'offset': 1 }
                                            ),
                                     ]),

                            ]),

            dbc.Tab(label='User-User Recommendations', children = [

                dbc.Row(
                    dbc.Col([   html.Hr(),
                                html.H5( "Enter user number (1 - " + str(df.user_id.max()) + ")", style={'text-align': 'left'}),
                                dbc.Input(
                                    id="message_input",
                                    value = '',
                                    type="text", 
                                    debounce=True
                                ),
                                html.Hr()
                            ],
                                width = {'size': 4, 'offset': 1 }
                            )
                        
                            

                    ),
                
                dbc.Row([dbc.Col([
                                html.Hr(),
                                html.H6( "Articles of the selected user: ", style={'text-align': 'left'}),
                            

                                dash_table.DataTable(
                                
                                    style_table={'height': '300px', 'overflowY': 'auto'},
                                    id='table_user_articles',
                                    columns = [{"name": i, "id": i} for i in return_user_articles(USER_TEMP, df, user_item).columns]
                                   ),
                                ],
                                width = {'size': 4, 'offset': 1 }),

                        dbc.Col([

                                    html.Hr(),
                                    dcc.Graph(id='hist_articles', figure={}),

                                ], width = {'size': 4, 'offset': 1 }
                                )]
                            
                        ),  
                                


                dbc.Row([dbc.Col([
                                html.Hr(),
                                html.H6( "Most similar neighbor users: ", style={'text-align': 'left'}),
                                dash_table.DataTable(
                                       
                                        #style_table={'height': '300px', 'overflowY': 'auto'},
                                        id='table_neighbors',
                                        columns=[{"name": i, "id": i} for i in get_top_sorted_users(USER_TEMP, df, user_item).head(10).columns]
                                        ),
                                html.Hr()
    
                                    ], width = {'size': 4, 'offset': 1 },
                                ),
                            dbc.Col([
                                html.Hr(),
                                html.H6( "New Recommended Articles: ", style={'text-align': 'left'}),
                                dash_table.DataTable(
                                       
                                        #style_table={'height': '300px', 'overflowY': 'auto'},
                                        id='table_recommendations',
                                        columns=[{"name": i, "id": i} for i in user_user_recs_part2(USER_TEMP, df , user_item).head(10).columns]
                                        ),
                                html.Hr()
    
                                    ], width = {'size': 4, 'offset': 1 },
                                )]
                        ),

             
                    
    
            ]),
            ])),
    ),
 

])



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id="table_user_articles", component_property="data"), Output(component_id="table_neighbors", component_property="data"),
     Output(component_id="hist_articles", component_property="figure"), Output(component_id="table_recommendations", component_property="data")],
    [Input(component_id='message_input', component_property='value')]
)
def updateTable_articles(sel_user):

    sel_user = float(sel_user)
    
    data_articles = return_user_articles(sel_user, df, user_item)

    data_neighbors = get_top_sorted_users(sel_user, df, user_item).head(10).to_dict('records')

    df_group = data_articles.groupby(['article_id', 'title'])['article_id'].count().sort_values(ascending = False)

    fig = px.bar(x = df_group.index.get_level_values(0).map(lambda x: 'id:' + str(x)), y = df_group, hover_data=[ df_group.index.get_level_values(1)], height=400)
    
    fig.update_layout(

        xaxis_title="User: " + str(sel_user)+ " Articles",
        yaxis_title="Number of interactions",

        )

    fig.update_layout(plot_bgcolor = BGCOLOR, paper_bgcolor = BGCOLOR)

    data_rec = user_user_recs_part2(sel_user, df,  user_item).to_dict('records')

    return data_articles.to_dict('records'), data_neighbors, fig, data_rec


    


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)