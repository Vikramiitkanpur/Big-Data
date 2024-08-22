import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from wordcloud import WordCloud
from flask import Flask
from distribution_of_users import generate_sunburst_chart
from wordcloud_of_tags import update_wordcloud
from genre_wise_movie_releases_over_time import update_plot_genre
from MovieGenreDistributionByAgeGroup import update_pie_chart_movie
from genre_vs_genre_analysis import get_genre_vs_genre_analysis
from movie_recommendation import recommended_plot

## Need for movie recommender
# Load data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')
new_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()
tags = pd.read_csv('tags.csv')
tags.sort_values(by='movieId')
new_tags = tags.groupby('movieId')['tag'].apply(list).reset_index()
movies_tags = movies.merge(new_tags, on='movieId')
movies_tags_ratings = movies_tags.merge(new_ratings, on='movieId')

# Define functions
def gen(obj):
    genres_list = obj.split('|')
    return genres_list

def movie_title(movie_string):
    parts = movie_string.split(" (")
    return parts[0]

# Clean data
movies_tags_ratings['genres'] = movies_tags_ratings['genres'].apply(gen)
movies_tags_ratings['genres'] = movies_tags_ratings['genres'].apply(lambda x: [i.replace(' ', '') for i in x])
movies_tags_ratings['tag'] = movies_tags_ratings['tag'].apply(lambda x: [i.replace(' ', '') if isinstance(i, str) else i for i in x])
movies_tags_ratings['title'] = movies_tags_ratings['title'].apply(movie_title)
movies_tags_ratings['tags'] = movies_tags_ratings['genres'] + movies_tags_ratings['tag']

# Merge and process data
new_movies_df = movies_tags_ratings[['movieId', 'title', 'tags']]
new_movies_df['tags'] = new_movies_df['tags'].apply(lambda x: " ".join(str(tag) for tag in x))
new_movies_df['tags'] = new_movies_df['tags'].apply(lambda x: x.lower())
movie_options = [{'label': f"{title}", 'value': f"{title}"} for title in new_movies_df['title']]

##



#### Implemented by Abhishek


#this code is required for the genre vs genre analysis to work
genre_dict={'Mystery': 1514, 'Comedy': 8374, 'Documentary': 2471, 'War': 1194, 'Adventure': 2329, 'Drama': 13344, 'Animation': 1027, 'Sci-Fi': 1743, 'Film-Noir': 330, 'Romance': 4127, 'Thriller': 4178, 'Musical': 1036, 'Horror': 2611, 'IMAX': 196, 'Crime': 2939, 'Fantasy': 1412, '(no genres listed)': 246, 'Western': 676, 'Children': 1139, 'Action': 3520}
ratings_sum={'Adventure': 15339519.0, 'Children': 5688990.5, 'Fantasy': 7402463.5, 'Drama': 32546369.5, 'Mystery': 5705116.5, 'Sci-Fi': 10826318.5, 'Thriller': 18635056.5, 'Crime': 12119823.0, 'Action': 19334567.5, 'Comedy': 25702738.5, 'Romance': 13465940.5, 'War': 3994742.5, 'Horror': 4859261.0, 'Musical': 3098794.5, 'Western': 1512870.0, 'Animation': 4125665.0, 'IMAX': 1800063.5, 'Film-Noir': 859254.5, 'Documentary': 914806.0, '(no genres listed)': 1085.5}
rating_count={'Adventure': 4380351, 'Children': 1669249, 'Fantasy': 2111403, 'Drama': 8857853, 'Mystery': 1557282, 'Sci-Fi': 3150141, 'Thriller': 5313506, 'Crime': 3298335, 'Action': 5614208, 'Comedy': 7502234, 'Romance': 3802002, 'War': 1048618, 'Horror': 1482737, 'Musical': 870915, 'Western': 423714, 'Animation': 1140476, 'IMAX': 492366, 'Film-Noir': 216689, 'Documentary': 244619, '(no genres listed)': 361}
genre_avg_ratings={'Mystery': 3.663508921312903, 'Comedy': 3.4260113054324886, 'Documentary': 3.7397176834178865, 'War': 3.8095307347384844, 'Adventure': 3.5018926565473865, 'Drama': 3.6742955093068264, 'Animation': 3.6174939235897994, 'Sci-Fi': 3.4367726714455005, 'Film-Noir': 3.96538126070082, 'Romance': 3.541802581902903, 'Thriller': 3.50711121809216, 'Musical': 3.558090628821412, 'Horror': 3.2772238097518307, 'IMAX': 3.655945983272606, 'Crime': 3.6745276025631113, 'Fantasy': 3.5059453358738244, '(no genres listed)': 3.0069252077562325, 'Western': 3.5704980246109406, 'Children': 3.4081137685270444, 'Action': 3.44386376493354}


# Sample data
data1 = genre_dict
data2 = genre_avg_ratings
data3 = rating_count

df1 = pd.DataFrame.from_dict(data1, orient='index', columns=['Count'])
df1['Genre'] = df1.index
df1.reset_index(drop=True, inplace=True)

df2 = pd.DataFrame.from_dict(data2, orient='index', columns=['Average Rating'])
df2['Genre'] = df2.index
df2.reset_index(drop=True, inplace=True)

df3 = pd.DataFrame.from_dict(data3, orient='index', columns=['Total Ratings'])
df3['Genre'] = df3.index
df3.reset_index(drop=True, inplace=True)
#Till Here


movies_df = pd.read_csv("movies.csv")
ratings_df = pd.read_csv("ratings.csv")
users_df = pd.read_csv("users.csv")
tags_df = pd.read_csv('tags.csv')
genome_tags_df = pd.read_csv('genome-tags.csv')
genome_scores_df = pd.read_csv('genome-scores.csv')

# Merge movie data with ratings
movie_ratings = pd.merge(movies_df, ratings_df, on='movieId')
# Convert timestamp to datetime
movie_ratings['timestamp'] = pd.to_datetime(movie_ratings['timestamp'], unit='s')
# Extract year from timestamp
movie_ratings['year'] = movie_ratings['timestamp'].dt.year

########################

# Create app
server = Flask(__name__)
app = dash.Dash(server=server)
# Define tab styles

tab_style = {
    'borderRadius': '10px 10px 0px 0px',
    'backgroundColor': '#007bff',
    'color': 'white',
    'fontWeight': 'bold',
    'padding': '12px 20px',
    'marginRight': '2px',
    'cursor': 'pointer',
    'fontSize': '16px'
}

tab_selected_style = {
    'borderTop': 'none',
    'borderBottom': '3px solid #007bff',
    'backgroundColor': '#007bff',
    'color': 'white',
    'fontWeight': 'bold',
    'padding': '12px 20px',
    'marginRight': '2px',
    'cursor': 'pointer',
    'fontSize': '16px'
}
graph_style = {
    'font_family': 'Arial',
    'background_color': '#f9f9f9',
    'plot_background_color': '#ffffff',
    'grid_color': '#e0e0e0',
    'title_font_size': 20,
    'title_font_color': '#333333',
    'xaxis_title_font_size': 14,
    'xaxis_title_font_color': '#666666',
    'yaxis_title_font_size': 14,
    'yaxis_title_font_color': '#666666',
}
# Define age range options (multiples of 5)
age_range_options = [{'label': str(i), 'value': i} for i in range(10, 91) if i % 5 == 0]

app.layout = html.Div(style={'backgroundColor': '#f0f0f0'},children=[
    html.H1('MOVIE ANALYSIS', style={'textAlign': 'center', 'color': '#ffffff', 'fontFamily': 'Arial, sans-serif', 'marginBottom': '20px', 'fontSize': '36px', 'fontWeight': 'bold', 'backgroundColor': '#007bff', 'padding': '20px'}),
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='MOVIE RECOMMENDATION', value='tab1', style={'font-weight': 'bold', 'backgroundColor': '#ffffff', 'marginBottom': '10px', 'width': '200px', 'textAlign': 'center'},
            selected_style={'backgroundColor': '#f0f0f0'}, children=[
            html.Div([
               dcc.Dropdown(
                id='movie-dropdown-recommender',
                options=movie_options,
                value=movie_options[0]['value']
                ),
                html.Div(id='output-graph'),
            ])
        ]),
        dcc.Tab(
            label='USER-DISTRIBUTION',
            value='tab2',
            style={'font-weight': 'bold', 'backgroundColor': '#ffffff', 'marginBottom': '10px', 'width': '200px', 'textAlign': 'center'},
            selected_style={'backgroundColor': '#f0f0f0'},
            children=[
                html.Div([
                    html.H2("User Distribution for Each Movie", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id='movie-dropdown',
                        options=[{'label': movie_title, 'value': movie_id} for movie_id, movie_title in zip(movies_df['movieId'], movies_df['title'])],
                        placeholder="Select a movie"
                    ),
                    html.Div([
                        html.Label('Layer 1:'),
                        dcc.Dropdown(
                            id='layer1-dropdown',
                            options=[
                                {'label': 'Gender', 'value': 'gender'},
                                {'label': 'Age Group', 'value': 'age_group'},
                                {'label': 'Occupation', 'value': 'occupation'}
                            ],
                            placeholder="Layer 1",
                            multi=False,
                            style={'width': '30%', 'display': 'inline-block', 'margin-right': '5px'}
                        ),
                    ]),
                    html.Div([
                        html.Label('Layer 2:'),
                        dcc.Dropdown(
                            id='layer2-dropdown',
                            placeholder="Layer 2",
                            multi=False,
                            style={'width': '30%', 'display': 'inline-block', 'margin-right': '5px'}
                        ),
                    ]),
                    html.Div([
                        html.Label('Layer 3:'),
                        dcc.Dropdown(
                            id='layer3-dropdown',
                            placeholder="Layer 3",
                            multi=False,
                            style={'width': '30%', 'display': 'inline-block'}
                        ),
                    ]),
                    dcc.Graph(id='sunburst-chart')
                ])
            ]),
        dcc.Tab(label='MOVIE TAG WORDCLOUD', value='tab3', style={'font-weight': 'bold', 'backgroundColor': '#ffffff', 'marginBottom': '10px', 'width': '200px', 'textAlign': 'center'},
            selected_style={'backgroundColor': '#f0f0f0'}, children=[
            html.Div([
                html.H2("Movie Tag Wordcloud", style={'textAlign': 'center'}),
                dcc.Dropdown(
                    id='movie-dropdown-wordcloud',
                    options=[{'label': movie, 'value': movieId} for movieId, movie in zip(movies_df['movieId'][:990], movies_df['title'][:990])],
                    value=None,
                    placeholder="Select a movie"
                ),
                dcc.Graph(id='wordcloud-graph')
            ])
        ]),
        dcc.Tab(label='GENRE-LINE-PLOT', value='tab4',style={'font-weight': 'bold', 'backgroundColor': '#ffffff', 'marginBottom': '10px', 'width': '200px', 'textAlign': 'center'},
            selected_style={'backgroundColor': '#f0f0f0'}, children=[
            html.H2(children='Genre-wise Movie Releases Over Time', style={'textAlign': 'center'}),

            dcc.Graph(
                id='genre-line-plot',
                config={'displayModeBar': False}  # Hide the plotly modebar
            )
        ]),
        dcc.Tab(label='MOVIE-GENRE-DISTRIBUTION', value='tab5',style={'font-weight': 'bold', 'backgroundColor': '#ffffff', 'marginBottom': '10px', 'width': '200px', 'textAlign': 'center'},
            selected_style={'backgroundColor': '#f0f0f0'}, children=[
            html.H2("Movie Genre Distribution by Age Group", style={'textAlign': 'center'}),
            html.Div([
                html.Label('Minimum Age:'),
                dcc.Dropdown(
                    id='min-age-dropdown',
                    options=age_range_options,
                    value=10
                )
            ]),
            html.Div([
                html.Label('Maximum Age:'),
                dcc.Dropdown(
                    id='max-age-dropdown',
                    options=age_range_options,
                    value=20
                )
            ]),
            dcc.Graph(id='genre-pie-chart', style={'width': '100%', 'height': '80vh'})

        ]),
        dcc.Tab(label='GENRE VS GENRE', value='tab6',style={'font-weight': 'bold', 'backgroundColor': '#ffffff', 'marginBottom': '10px', 'width': '200px', 'textAlign': 'center'},
            selected_style={'backgroundColor': '#f0f0f0'}, children=[
            html.H2(children=''),

            html.H2("Genre vs Genre Analysis", style={'textAlign': 'center'}),
            html.Div([
                html.Div([
                    html.Label('Select Genre 1:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                    id='genre1-dropdown',
                    options=[{'label': genre, 'value': genre} for genre in df1['Genre']],
                    value='Action',
                    style={'width': '200px'}
                    ),
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([
                    html.Label('Select Genre 2:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='genre2-dropdown',
                        options=[{'label': genre, 'value': genre} for genre in df1['Genre']],
                        value='Comedy'
                    ),
                ], style={'width': '48%', 'display': 'inline-block'}),
            ]),
            html.Div([
                html.Div([
                    dcc.Graph(id='genre-count', config={'displayModeBar': False}),
                ], style={'width': '32%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='average-rating', config={'displayModeBar': False}),
                ], style={'width': '32%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='total-ratings', config={'displayModeBar': False}),
                ], style={'width': '32%', 'display': 'inline-block'}),
             ]),
        ]),
        ####### Implemented by Abhishek
        dcc.Tab(label='TEMPORAL ANALYSIS', value='tab7', style={'font-weight': 'bold', 'backgroundColor': '#ffffff', 'marginBottom': '10px', 'width': '200px', 'textAlign': 'center'},
            selected_style={'backgroundColor': '#f0f0f0'},children=[
                html.Div([
                    html.Div([
                        dcc.Graph(id='movie-rating-graph'),
                        html.P("Select Genre:"),
                        dcc.Dropdown(
                            id='genre-dropdown',
                            options=[{'label': genre, 'value': genre} for genre in movie_ratings['genres'].unique()],
                            value=movie_ratings['genres'].unique()[0]
                        )
                    ], className='six columns'),
                    html.Div([
                        dcc.Graph(id='user-rating-graph')
                    ], className='six columns')
                ], className='row'),

                html.Div([
                    html.Div([
                        dcc.Graph(id='average-rating-by-genre')
                    ], className='six columns'),
                    html.Div([
                        dcc.Graph(id='average-rating-by-year')
                    ], className='six columns')
                ], className='row')
            ]
        ),
        # Add other tabs here...
        
    ])
])






######################################################
@app.callback(
    Output('output-graph', 'children'),
    [Input('movie-dropdown-recommender', 'value')]
)
def recommend_movies(movie_name):
    return recommended_plot(movie_name)

@app.callback(
    Output('sunburst-chart', 'figure'),
    [Input('movie-dropdown', 'value'),
     Input('layer1-dropdown', 'value'),
     Input('layer2-dropdown', 'value'),
     Input('layer3-dropdown', 'value'),
     Input('tabs', 'value')]
)
def update_sunburst_chart(selected_movie_id, layer1, layer2, layer3, selected_tab):
    if selected_tab == 'tab1':
        return generate_sunburst_chart(selected_movie_id, layer1, layer2, layer3)
    else:
        return {}
# Callback to update the second and third dropdowns based on the first dropdown
@app.callback(
    Output('layer2-dropdown', 'options'),
    Output('layer2-dropdown', 'value'),
    Input('layer1-dropdown', 'value')
)
def update_layer2_options(selected_layer1):
    if selected_layer1 == 'gender':
        options = [
            {'label': 'Age Group', 'value': 'age_group'},
            {'label': 'Occupation', 'value': 'occupation'}
        ]
        value = 'age_group'
    elif selected_layer1 == 'age_group':
        options = [
            {'label': 'Gender', 'value': 'gender'},
            {'label': 'Occupation', 'value': 'occupation'}
        ]
        value = 'gender'
    elif selected_layer1 == 'occupation':
        options = [
            {'label': 'Gender', 'value': 'gender'},
            {'label': 'Age Group', 'value': 'age_group'}
        ]
        value = 'gender'
    else:
        options = []
        value = None
    
    return options, value

# Callback to update the third dropdown based on the first two dropdowns
@app.callback(
    Output('layer3-dropdown', 'options'),
    Output('layer3-dropdown', 'value'),
    Input('layer1-dropdown', 'value'),
    Input('layer2-dropdown', 'value')
)
def update_layer3_options(selected_layer1, selected_layer2):
    if selected_layer1 == 'gender':
        if selected_layer2 == 'age_group':
            options = [{'label': 'Occupation', 'value': 'occupation'}]
            value = 'occupation'
        elif selected_layer2 == 'occupation':
            options = [{'label': 'Age Group', 'value': 'age_group'}]
            value = 'age_group'
        else:
            options = []
            value = None
    elif selected_layer1 == 'age_group':
        if selected_layer2 == 'gender':
            options = [{'label': 'Occupation', 'value': 'occupation'}]
            value = 'occupation'
        elif selected_layer2 == 'occupation':
            options = [{'label': 'Gender', 'value': 'gender'}]
            value = 'gender'
        else:
            options = []
            value = None
    elif selected_layer1 == 'occupation':
        if selected_layer2 == 'gender':
            options = [{'label': 'Age Group', 'value': 'age_group'}]
            value = 'age_group'
        elif selected_layer2 == 'age_group':
            options = [{'label': 'Gender', 'value': 'gender'}]
            value = 'gender'
        else:
            options = []
            value = None
    else:
        options = []
        value = None
    
    return options, value

# Callback to update the wordcloud
@app.callback(
    Output('wordcloud-graph', 'figure'),
    [Input('movie-dropdown-wordcloud', 'value')]
)
def update_wordcloud_callback(movie_id):
    return update_wordcloud(movie_id)

#Callback to update_plot_for_genre
@app.callback(
    Output('genre-line-plot', 'figure'),
    [Input('genre-line-plot', 'clickData')]
)
def update_plot(clickData):
    return update_plot_genre(clickData)

# Define callback to update the pie chart based on selected age range
@app.callback(
    Output('genre-pie-chart', 'figure'),
    [Input('min-age-dropdown', 'value'),
     Input('max-age-dropdown', 'value')]
)
def update_pie_chart(min_age, max_age):
    return update_pie_chart_movie(min_age,max_age)

@app.callback(
    [Output('genre-count', 'figure'),
     Output('average-rating', 'figure'),
     Output('total-ratings', 'figure')],
    [Input('genre1-dropdown', 'value'),
     Input('genre2-dropdown', 'value')]
)
def update_genre_vs_genre(genre1,genre2):
    return get_genre_vs_genre_analysis(genre1,genre2)

# Temporal analysis implementation by Abhishek

@app.callback(
    dash.dependencies.Output('movie-rating-graph', 'figure'),
    [dash.dependencies.Input('genre-dropdown', 'value')]
)
def update_movie_rating_graph(selected_genre):
    data = movie_ratings[movie_ratings['genres'] == selected_genre]
    avg_rating = data.groupby('year')['rating'].mean().reset_index()
    return {
        'data': [go.Scatter(x=avg_rating['year'], y=avg_rating['rating'], mode='lines+markers')],
        'layout': go.Layout(title=f'Average Rating for {selected_genre} Movies Over Time',
                            xaxis=dict(title='Year'), yaxis=dict(title='Average Rating'),
                            template='plotly_dark')
    }

@app.callback(
    dash.dependencies.Output('user-rating-graph', 'figure'),
    [dash.dependencies.Input('genre-dropdown', 'value')]
)
def update_user_rating_graph(selected_genre):
    data = movie_ratings[movie_ratings['genres'] == selected_genre]
    user_count = data.groupby('year')['userId'].count().reset_index()
    return {
        'data': [go.Scatter(x=user_count['year'], y=user_count['userId'], mode='lines+markers')],
        'layout': go.Layout(title=f'Number of Ratings for {selected_genre} Movies Over Time',
                            xaxis=dict(title='Year'), yaxis=dict(title='Number of Ratings'),
                            template='plotly_dark')
    }

@app.callback(
    dash.dependencies.Output('average-rating-by-genre', 'figure'),
    [dash.dependencies.Input('genre-dropdown', 'value')]
)
def update_average_rating_by_genre(selected_genre):
    data = movie_ratings[movie_ratings['genres'] == selected_genre]
    genre_rating = data.groupby('genres')['rating'].mean().reset_index()
    return {
        'data': [go.Bar(x=genre_rating['genres'], y=genre_rating['rating'])],
        'layout': go.Layout(title=f'Average Rating for Each Genre - {selected_genre}',
                            xaxis=dict(title='Genre'), yaxis=dict(title='Average Rating'),
                            template='plotly_dark')
    }

@app.callback(
    dash.dependencies.Output('average-rating-by-year', 'figure'),
    [dash.dependencies.Input('genre-dropdown', 'value')]
)
def update_average_rating_by_year(selected_genre):
    data = movie_ratings[movie_ratings['genres'] == selected_genre]
    year_rating = data.groupby('year')['rating'].mean().reset_index()
    return {
        'data': [go.Bar(x=year_rating['year'], y=year_rating['rating'])],
        'layout': go.Layout(title=f'Average Rating Over Time for {selected_genre} Movies',
                            xaxis=dict(title='Year'), yaxis=dict(title='Average Rating'),
                            template='plotly_dark')
    }

####################

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

