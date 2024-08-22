import plotly.graph_objs as go
import pandas as pd

movie_df = pd.read_csv('movies.csv')
genre_mappings = {
    'Action': 'Action/Adventure',
    'Adventure': 'Action/Adventure',
    'Animation': 'Animation/Family',
    'Children': 'Animation/Family',
    'Fantasy': 'Animation/Family',
    'Crime': 'Crime/Thriller',
    'Thriller': 'Crime/Thriller',
    'Mystery': 'Mystery/Film-Noir',
    'Horror': 'Horror/Sci-Fi',
    'Sci-Fi': 'Horror/Sci-Fi',
    'War': 'War/Drama',
    'Drama': 'War/Drama',
    'Musical': 'Music/Romance',
    'Romance': 'Music/Romance',
    'Film-Noir':'Mystery/Film-Noir' ,
    'Documentary': 'Documentary',
    'Western': 'Other',
    'Comedy' : 'Other',
    'IMAX' : 'Other'
}
movie_data = {
    'Crime/Thriller': {year: 0 for year in range(1995, 2013)},
    'Horror/Sci-Fi': {year: 0 for year in range(1995, 2013)},
    'War/Drama': {year: 0 for year in range(1995, 2013)},
    'Action/Adventure': {year: 0 for year in range(1995, 2013)},
    'Other': {year: 0 for year in range(1995, 2013)},
    'Animation/Family': {year: 0 for year in range(1995, 2013)},
    'Documentary': {year: 0 for year in range(1995, 2013)},
    'Mystery/Film-Noir': {year: 0 for year in range(1995, 2013)},
    'Music/Romance': {year: 0 for year in range(1995, 2013)}
}

for title,genres in zip(movie_df['title'],movie_df['genres']):
    year = ''.join(filter(str.isdigit, title.split("(")[-1]))
    if(year==''):
        continue
    if((int(year)>=1995 and int(year)<=2012) and genres!='(no genres listed)'):
        genre_list = list(genres.split('|'))
        for genre in genre_list:
            movie_data[genre_mappings[genre]][int(year)] += 1

def update_plot_genre(clickData):
    if clickData is None or 'curveNumber' not in clickData['points'][0]:
        selected_genres = list(movie_data.keys())  # Show all genres by default
    else:
        selected_genres = [list(movie_data.keys())[clickData['points'][0]['curveNumber']]]

    traces = []
    for genre in selected_genres:
        x = list(movie_data[genre].keys())
        y = list(movie_data[genre].values())
        traces.append(go.Scatter(x=x, y=y, mode='lines', name=genre))

    layout = go.Layout(
        #title='Genre-wise Movie Releases Over Time',
        xaxis=dict(title='Year', dtick=2),  # Show every year on the x-axis
        yaxis=dict(title='Number of Movies Released'),
        legend=dict(x=1.1, y=1, orientation="v")  # Position legend on the right side
    )

    return {'data': traces, 'layout': layout}
