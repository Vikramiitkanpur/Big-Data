import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
movies_df = pd.read_csv("movies.csv")
ratings_df = pd.read_csv("ratings.csv")
users_df = pd.read_csv("users.csv")

# Function to group ages into 10-year intervals
def age_group(age):
    if age >= 10 and age < 20:
        return "10-19"
    elif age >= 20 and age < 30:
        return "20-29"
    elif age >= 30 and age < 40:
        return "30-39"
    elif age >= 40 and age < 50:
        return "40-49"
    elif age >= 50 and age < 60:
        return "50-59"
    elif age >= 60:
        return "60+"
    else:
        return "Unknown"

# Apply age grouping
users_df['age_group'] = users_df['age'].apply(age_group)

# Define a function to generate sunburst chart
def generate_sunburst_chart(selected_movie_id, layer1, layer2, layer3):
    # print("rama chandra")
    if selected_movie_id is None or layer1 is None or layer2 is None or layer3 is None:
        return {}
    
    # Filter ratings for the selected movie
    ratings_for_movie = ratings_df[ratings_df['movieId'] == selected_movie_id]
    
    # Get unique user ids for the selected movie
    user_ids_for_movie = ratings_for_movie['userId'].unique()
    
    # Filter users data for the selected users
    users_for_movie = users_df[users_df['userId'].isin(user_ids_for_movie)]

    # Group users by the selected layers and count the number of users in each group
    group_cols = [layer1, layer2, layer3]
    user_counts = users_for_movie.groupby(group_cols).size().reset_index(name='user_count')

    # Create the sunburst chart based on selected layers
    fig = px.sunburst(user_counts, path=group_cols, values='user_count')

    # Update hover template to show count of users
    fig.update_traces(hovertemplate='<b>%{label}</b><br>user_count: %{value}')
    # print(fig)
    return fig
