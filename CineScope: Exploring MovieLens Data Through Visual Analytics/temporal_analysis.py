import pandas as pd
import plotly.graph_objs as go


# Load movie data
movies = pd.read_csv('movies.csv')

# Assuming you have a ratings dataset with columns: userId, movieId, rating, timestamp
ratings = pd.read_csv('ratings.csv')

# Merge movie data with ratings
movie_ratings = pd.merge(movies, ratings, on='movieId')
# Convert timestamp to datetime
movie_ratings['timestamp'] = pd.to_datetime(movie_ratings['timestamp'], unit='s')
# Extract year from timestamp
movie_ratings['year'] = movie_ratings['timestamp'].dt.year



def update_graphs(selected_genre):
    # Filter data by selected genre
    data = movie_ratings[movie_ratings['genres'] == selected_genre]
    
    # Calculate average rating by year
    avg_rating_by_year = data.groupby('year')['rating'].mean().reset_index()
    
    # Calculate number of ratings by year
    user_rating_count = data.groupby('year')['userId'].count().reset_index()
    
    # Calculate average rating by genre
    avg_rating_by_genre = data.groupby('genres')['rating'].mean().reset_index()
    
    # Define common layout
    layout = go.Layout(
        xaxis=dict(title='Year'),
        template='plotly_dark'
    )
    
    # Define figures for each graph
    movie_rating_figure = {
        'data': [go.Scatter(x=avg_rating_by_year['year'], y=avg_rating_by_year['rating'], mode='lines+markers')],
        'layout': {**layout, 'title': f'Average Rating for {selected_genre} Movies Over Time',
                   'yaxis': dict(title='Average Rating')}
    }
    
    user_rating_figure = {
        'data': [go.Scatter(x=user_rating_count['year'], y=user_rating_count['userId'], mode='lines+markers')],
        'layout': {**layout, 'title': f'Number of Ratings for {selected_genre} Movies Over Time',
                   'yaxis': dict(title='Number of Ratings')}
    }
    
    avg_rating_by_genre_figure = {
        'data': [go.Bar(x=avg_rating_by_genre['genres'], y=avg_rating_by_genre['rating'])],
        'layout': {**layout, 'title': f'Average Rating for Each Genre - {selected_genre}',
                   'xaxis': dict(title='Genre'), 'yaxis': dict(title='Average Rating')}
    }
    
    avg_rating_by_year_figure = {
        'data': [go.Bar(x=avg_rating_by_year['year'], y=avg_rating_by_year['rating'])],
        'layout': {**layout, 'title': f'Average Rating Over Time for {selected_genre} Movies',
                   'yaxis': dict(title='Average Rating')}
    }
    
    return movie_rating_figure, user_rating_figure, avg_rating_by_genre_figure, avg_rating_by_year_figure


# Count unique genre combinations
#unique_genre_combinations = movie_ratings['genres'].nunique()
#print("Number of unique genre combinations:", unique_genre_combinations)

