import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from fuzzywuzzy import process

# Read CSV files into dataframes
ratings_df = pd.read_csv('ratings.csv')
movies_df = pd.read_csv('movies.csv')
all_titles = movies_df['title'].tolist()

def movie_finder(title):
    return process.extractOne(title,all_titles)[0]

# Compute Bayesian average
movie_stats = ratings_df.groupby('movieId')['rating'].agg(['count', 'mean'])
C = movie_stats['count'].mean()
m = movie_stats['mean'].mean()

def bayesian_avg(ratings):
    return round((C * m + ratings.sum()) / (C + ratings.count()), 3)

average_ratings_df = ratings_df.groupby('movieId')['rating'].agg(bayesian_avg).reset_index()
average_ratings_df.columns = ['movieId', 'average_rating']

# Genre mappings
genre_mappings = {
    'Action': 'Action/Adventure',
    'Adventure': 'Action/Adventure',
    'Animation': 'Animation/Children',
    'Children': 'Animation/Children',
    'Fantasy': 'Fantasy/Western',
    'Crime': 'Crime/Thriller',
    'Thriller': 'Crime/Thriller',
    'Mystery': 'Mystery/Film-Noir',
    'Horror': 'Horror/Sci-Fi',
    'Sci-Fi': 'Horror/Sci-Fi',
    'War': 'War/Drama',
    'Drama': 'War/Drama',
    'Musical': 'Music/Romance',
    'Romance': 'Music/Romance',
    'Film-Noir': 'Mystery/Film-Noir',
    'Documentary': 'Documentary/IMAX',
    'IMAX': 'Documentary/IMAX',
    'Western': 'Fantasy/Western'
}

# Function to combine genres based on mappings
def combine_genres(genres):
    return '|'.join(genre_mappings.get(genre, '') for genre in genres.split('|'))

# Apply genre combination function to the dataset
movies_df['combined_genres'] = movies_df['genres'].apply(combine_genres)

# Merge ratings and movies data
combined_df = pd.merge(ratings_df, movies_df, on='movieId')

# Split the combined genres into individual genres
split_genres = combined_df['combined_genres'].str.split('|')

# Remove duplicates from each list of genres
unique_genres = split_genres.apply(set)

# Join the unique genres back together with "|"
cleaned_genres = unique_genres.apply('|'.join)

# Replace the combined_genres column with the cleaned genres
combined_df['combined_genres'] = cleaned_genres

# Get unique genres
all_genres = set('|'.join(movies_df['combined_genres']).split('|')) - {''}

unique_genres_list=all_genres


def plot_user_genre_preferences(user_id):
    num_movies_genres = {}

    # Step 1: Filter ratings by the specific user
    user_ratings = combined_df[combined_df['userId'] == user_id]

    for combined_genre in unique_genres_list:
        num_movies_genres[combined_genre] = []
        individual_genres = combined_genre.split('/')
        if len(individual_genres) == 2:
            num_movies_combined_genre = user_ratings[user_ratings['combined_genres'].str.contains(individual_genres[0])].shape[0]
            num_movies_genres[combined_genre].append(num_movies_combined_genre)
            num_movies_action_not_adventure = user_ratings[user_ratings['genres'].str.contains(individual_genres[0]) & ~user_ratings['genres'].str.contains(individual_genres[1])].shape[0]
            num_movies_genres[combined_genre].append(num_movies_action_not_adventure)
            num_movies_adventure_not_action = user_ratings[user_ratings['genres'].str.contains(individual_genres[1]) & ~user_ratings['genres'].str.contains(individual_genres[0])].shape[0]
            num_movies_genres[combined_genre].append(num_movies_adventure_not_action)
            num_movies_adventure_action = user_ratings[user_ratings['genres'].str.contains(individual_genres[0]) & user_ratings['genres'].str.contains(individual_genres[1])].shape[0]
            num_movies_genres[combined_genre].append(num_movies_adventure_action)

    # Define the data
    data = {
        'parent': [],
        'character': [],
        'value': []
    }

    # Iterate over the dictionary and format the data
    for parent, values in num_movies_genres.items():
        genres = parent.split('/')
        genres.append("Both")
        for i, genre in enumerate(genres):
            j = i + 1
            data['parent'].append(parent)
            data['character'].append(genre)
            data['value'].append(values[j])

    # Create DataFrame
    data_df = pd.DataFrame(data)

    # Plotting
    fig = px.sunburst(data_df, path=['parent', 'character'], values='value', 
                      title=f'Sunburst Chart of Genres and Sub-Genres for User {user_id}')
    return fig

# Initialize an empty dictionary to store users fond of each genre
users_fond_of_genre = {}

# Loop through each genre in unique_genres_list
for genre in all_genres:
    # Filter the dataset to include only rows where the movie belongs to the current genre
    genre_movies_df = combined_df[combined_df['combined_genres'].str.contains(genre)]
    
    # Group the filtered dataset by user ID and count the number of unique movies each user has rated
    genre_movie_counts = genre_movies_df.groupby('userId')['movieId'].nunique()

    # Calculate the 95th percentile value for the current genre
    percentile_95 = genre_movie_counts.quantile(0.98)
    
    # Identify users who have rated a significant number of movies for the current genre
    threshold = percentile_95  # Using the 95th percentile value as the threshold
    users_fond_of_current_genre = genre_movie_counts[genre_movie_counts >= threshold].index.tolist()
    
    # Store the list of users in the dictionary with the genre as the key
    users_fond_of_genre[genre] = users_fond_of_current_genre
    del genre_movies_df

    
def get_horizontal_bar_chart(movie_list):

    movies_list = [movie_finder(movie) for movie in movie_list]

    # print(movies_list)
    filtered_df = movies_df[movies_df['title'].isin(movie_list)]
    
    numbers_list = [int(movies_df[movies_df['title'] == title]['movieId']) for title in movies_list]

    movie_list = numbers_list
    # print(numbers_list)
    # Calculate average ratings for each genre for each movie
    genre_average_ratings = {}
    for random_movie_id in numbers_list:
        movie_row = combined_df[combined_df['movieId'] == random_movie_id]
        genres = movie_row['combined_genres'].iloc[0].split('|')
        if '' in genres:
            genres.remove('')
        genre_average_ratings[random_movie_id] = {}
        for genre in genres:
            filtered_ratings = combined_df[(combined_df['userId'].isin(users_fond_of_genre[genre])) & (combined_df['movieId'] == random_movie_id)]
            average_rating = filtered_ratings['rating'].mean()
            if average_rating == 0:
                average_rating = average_ratings_df.loc[average_ratings_df['movieId'] == random_movie_id, 'average_rating'].iloc[0]
            genre_average_ratings[random_movie_id][genre] = average_rating
        for genre in all_genres:
            if genre not in genres:
                genre_average_ratings[random_movie_id][genre] = 0

    # print(genre_average_ratings)


    #import plotly.graph_objects as go


    data=genre_average_ratings
    # Initialize lists to store x and y values
    x_values = []
    x_values1 = []
    x_values2 = []
    x_values3 = []
    x_values4 = []
    x_values5 = []
    x_values6 = []
    x_values7 = []
    x_values8 = []
    x_values9 = []

    y_values = movies_list

    # Extract ratings for each genre for each movie
    for movie_id, genre_ratings in data.items():
        for genre, rating in genre_ratings.items():
            if genre == 'Animation/Children':
                x_values.append(rating)
            elif genre == 'Action/Adventure':
                x_values1.append(rating)
            elif genre == 'War/Drama':
                x_values2.append(rating)
            elif genre == 'Documentary':
                x_values3.append(rating)
            elif genre == 'Crime/Thriller':
                x_values4.append(rating)
            elif genre == 'Documentary/IMAX':
                x_values5.append(rating)
            elif genre == 'Music/Romance':
                x_values6.append(rating)
            elif genre == 'Horror/Sci-Fi':
                x_values7.append(rating)
            elif genre == 'Fantasy/Western':
                x_values8.append(rating)
            elif genre == 'Mystery/Film-Noir':
                x_values9.append(rating)

    print(x_values)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values,
        name='Animation/Children',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values1,
        name='Action/Adventure',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values2,
        name='War/Drama',
        orientation='h',
        marker=dict(
            color='rgba(0, 100, 0, 0.6)',
            line=dict(color='rgba(0, 100, 0, 1)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values3,
        name='Documentary',
        orientation='h',
        marker=dict(
            color='rgba(0, 0, 100, 0.6)',
            line=dict(color='rgba(0, 0, 100, 1)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values4,
        name='Crime/Thriller',
        orientation='h',
        marker=dict(
            color='rgba(100, 0, 0, 0.6)',
            line=dict(color='rgba(100, 0, 0, 1)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values5,
        name='Documentary/IMAX',
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 10, 0.6)',
            line=dict(color='rgba(255, 0, 10, 1)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values6,
        name='Music/Romance',
        orientation='h',
        marker=dict(
            color='rgba(96, 89, 161, 0.6)',
            line=dict(color='rgba(96, 89, 161, 1)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values7,
        name='Horror/Sci-Fi',
        orientation='h',
        marker=dict(
            color='rgba(122, 255, 153, 0.6)',
            line=dict(color='rgba(122, 255, 153, 1)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values8,
        name='Fantasy/Western',
        orientation='h',
        marker=dict(
            color='rgba(122, 255, 255, 0.6)',
            line=dict(color='rgba(122, 255, 255, 1)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=y_values,
        x=x_values9,
        name='Mystery/Film-Noir',
        orientation='h',
        marker=dict(
            color='rgba(252, 101, 0, 0.6)',
            line=dict(color='rgba(252, 101, 0, 1)', width=3)
        )
    ))


    fig.update_layout(barmode='stack')

    return fig

