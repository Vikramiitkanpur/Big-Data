import pandas as pd
import plotly.express as px

# Load the datasets
users_df = pd.read_csv("users.csv")
movies_df = pd.read_csv("movies.csv")

# Genre mappings
genre_mappings = {
    'Action': 'Action/Adventure',
    'Adventure': 'Action/Adventure',
    'Animation': 'Animation/Family',
    'Children': 'Animation/Family',
    'Fantasy': 'Animation/Family',
    'Crime': 'Crime/Thriller',
    'Thriller': 'Crime/Thriller',
    'Mystery': 'Mystery/Film-Noir',
    'Film-Noir': 'Mystery/Film-Noir',
    'Horror': 'Horror/Sci-Fi',
    'Sci-Fi': 'Horror/Sci-Fi',
    'War': 'War/Drama',
    'Drama': 'War/Drama',
    'Musical': 'Music/Romance',
    'Romance': 'Music/Romance',
    'Documentary': 'Documentary',
    'Western': 'Western'
}

# Merge genres according to mappings and remove "no genres listed"
movies_df['genres'] = movies_df['genres'].apply(lambda x: '|'.join(genre_mappings.get(genre, genre) for genre in x.split('|')))

# Define age range options (multiples of 5)
age_range_options = [{'label': str(i), 'value': i} for i in range(10, 91) if i % 5 == 0]

def update_pie_chart_movie(min_age, max_age):
    filtered_users = users_df[(users_df['age'] >= min_age) & (users_df['age'] <= max_age)]
    merged_df = pd.merge(filtered_users, movies_df, how='inner', left_on='userId', right_on='movieId')
    genre_counts = merged_df['genres'].str.get_dummies(sep='|').sum().sort_values(ascending=False)
    genre_counts = genre_counts.reset_index()
    genre_counts.columns = ['Genre', 'Count']
    
    # Remove rows with no genres listed
    genre_counts = genre_counts[genre_counts['Genre'] != '']
    
    # Group by the first genre in merged genres for legend
    genre_counts['Legend'] = genre_counts['Genre'].apply(lambda x: x.split('/')[0])
    genre_counts = genre_counts.groupby('Legend', as_index=False)['Count'].sum()
    
    fig = px.pie(genre_counts, values='Count', names='Legend', title=f"Genre Distribution for Age {min_age}-{max_age} Group")
    return fig
