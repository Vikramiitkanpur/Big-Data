import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

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

def get_genre_vs_genre_analysis(genre1, genre2):
    df = pd.DataFrame({
        'Genre': [genre1, genre2],
        'Count': [df1.loc[df1['Genre'] == genre1, 'Count'].values[0], df1.loc[df1['Genre'] == genre2, 'Count'].values[0]],
        'Average Rating': [df2.loc[df2['Genre'] == genre1, 'Average Rating'].values[0], df2.loc[df2['Genre'] == genre2, 'Average Rating'].values[0]],
        'Total Views': [df3.loc[df3['Genre'] == genre1, 'Total Ratings'].values[0], df3.loc[df3['Genre'] == genre2, 'Total Ratings'].values[0]]
    })

    fig_count = go.Figure(go.Bar(x=df['Genre'], y=df['Count'], name='Genre Movie Counts'))
    fig_count.update_traces(marker_color='#3182bd', marker_line_color='#3182bd', marker_line_width=1, opacity=0.8)

    fig_avg_rating = go.Figure(go.Bar(x=df['Genre'], y=df['Average Rating'], name='Average Rating by Genre'))
    fig_avg_rating.update_traces(marker_color='#e6550d', marker_line_color='#e6550d', marker_line_width=1, opacity=0.8)

    fig_total_ratings = go.Figure(go.Bar(x=df['Genre'], y=df['Total Views'], name='Total Views by Genre'))
    fig_total_ratings.update_traces(marker_color='#31a354', marker_line_color='#31a354', marker_line_width=1, opacity=0.8)

    for fig in [fig_count, fig_avg_rating, fig_total_ratings]:
        fig.update_layout(
            font_family='Arial',
            plot_bgcolor='#f9f9f9',
            paper_bgcolor='#f9f9f9',
            xaxis_title_font=dict(size=14, color='#666666'),
            yaxis_title_font=dict(size=14, color='#666666'),
            legend_font=dict(size=12, color='#666666'),
            title=dict(x=0.5, text='Genre vs Genre Analysis', font=dict(size=20, color='#333333'), xanchor='center', yanchor='top')
        )

    return fig_count, fig_avg_rating, fig_total_ratings
