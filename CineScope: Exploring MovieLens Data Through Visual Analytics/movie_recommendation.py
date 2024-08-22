# recommended_plot
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# Calculate similarity
cv = CountVectorizer(max_features=100, stop_words='english')
vector = cv.fit_transform(new_movies_df['tags']).toarray()
similarity = cosine_similarity(vector)

def recommend_movie(movie):
    index = new_movies_df[new_movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    return distances[1:11]

def get_recommeded_movies(movie_name):
    recommendations = recommend_movie(movie_name)
    x = [item[0] for item in recommendations]
    movie_titles = [new_movies_df.iloc[i].title for i in x]
    return movie_titles



def recommended_plot(movie_name):
    # Get the index of the movie
    index = new_movies_df[new_movies_df['title'] == movie_name].index[0]

    # Get recommendations for the movie
    recommendations = recommend_movie(movie_name)
    x = [item[0] for item in recommendations]
    movie_titles = [new_movies_df.iloc[i].title for i in x]
    similarity_scores = [item[1] for item in recommendations]

    # Create the plot
    fig = go.Figure([go.Bar(x=movie_titles, y=similarity_scores)])
	# fig.update_layout(title='Recommended Movie with their similarity with movie')
    fig.update_xaxes(title='Movie Title')
    fig.update_yaxes(title='Similarity Score')

    return dcc.Graph(figure=fig)

