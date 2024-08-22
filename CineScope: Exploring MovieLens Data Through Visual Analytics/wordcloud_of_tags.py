import plotly.graph_objs as go
from wordcloud import WordCloud
from dash.dependencies import Input, Output
import pandas as pd

tags_df = pd.read_csv('tags.csv')
genome_tags_df = pd.read_csv('genome-tags.csv')
genome_scores_df = pd.read_csv('genome-scores.csv')

def update_wordcloud(movie_id):
    if movie_id is None:
        return {}
    
    # Filter tags for selected movie
    movie_tags = tags_df[tags_df['movieId']==movie_id].tag
    
    tag_mapping = dict(zip(genome_tags_df['tag'], genome_tags_df['tagId']))
    
    final_tags = []
    list_of_tagIds = []
    for tag in movie_tags:
        if tag in tag_mapping and tag not in final_tags:
            final_tags.append(tag)
            list_of_tagIds.append(tag_mapping[tag])
    
    filtered_df = genome_scores_df[(genome_scores_df['movieId'] == movie_id) & (genome_scores_df['tagId'].isin(list_of_tagIds))]
    relevance_values = dict(zip(filtered_df['tagId'], filtered_df['relevance']))

    final_dictionary = {}
    for i in range(0,len(final_tags)):
        final_dictionary[final_tags[i]] = relevance_values[list_of_tagIds[i]]

    wordcloud_data = final_dictionary

    # Generate wordcloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)

    # Convert wordcloud to Plotly figure
    plotly_wordcloud = go.Figure(go.Image(z=wordcloud.to_array()))

    # Update layout to hide axis
    plotly_wordcloud.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    return plotly_wordcloud
