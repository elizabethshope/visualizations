# Imports
import pandas as pd
from nltk import word_tokenize, FreqDist
import regex as re
from nltk.corpus import stopwords
import plotly.graph_objs as go
import plotly.plotly as py
import numpy as np

# Read in data
terrorism_2016 = pd.read_csv('terrorism_2016_summaries.csv', encoding='latin1')

# Get list of regions
regions = pd.unique(terrorism_2016['region_txt'])

# Define regexes
numbers = re.compile("\d")
alpha = re.compile("\w")

# Concatenate summaries for each region & extract 10 most common words - put into dict
most_common_dict = {}

for region in regions:
    summaries = terrorism_2016['summary'][terrorism_2016['region_txt'] == region]
    summaries_concat = ' '.join(summaries)
    tokens = word_tokenize(summaries_concat)

    # Remove any tokens containing numeric chars
    tokens_cleaned = [token for token in tokens if not re.match(numbers, token)]

    # Remove any tokens that don't contain an alphabetical char
    tokens_cleaned = [token for token in tokens_cleaned if re.match(alpha, token)]

    # Make all tokens lowercase
    tokens_cleaned = [token.lower() for token in tokens_cleaned]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens_cleaned = [token for token in tokens_cleaned if token not in stop_words]

    # Determine frequency distribution
    fdist = FreqDist(tokens_cleaned)
    most_common = fdist.most_common(10)

    words = [item[0] for item in most_common]
    counts = [item[1] for item in most_common]

    most_common_dict[region] = {'words': words, 'counts': counts}

# Get the ones just for the middle east and north africa
words = most_common_dict['Middle East & North Africa']['words']
counts = most_common_dict['Middle East & North Africa']['counts']
sizes = (np.asarray(counts)/100).tolist()
ranks = [i for i in range(1, 11)]
hover_text = ['<b>Word:</b> %s<br><b>Rank:</b> %d<br><b>Occurrences:</b> %d' % (word, rank, count) for
              word, rank, count in zip(words, ranks, counts)]
bold_words = ['<b>%s</b>' % word for word in words]

# Make scatter plot with labeled
trace1 = go.Scatter(
    x=[1]*10,
    y=[i for i in range(1, 11)],
    mode='markers',
    text=hover_text,
    hoverinfo='text',
    hoverlabel=dict(
        font=dict(
            family='Raleway, sans-serif')
    ),
    marker=dict(
        size=sizes
    )
)

trace2 = go.Scatter(
    x=[1]*10,
    y=[i for i in range(1, 11)],
    mode='text',
    text=bold_words,
    textposition='middle-center',
    hoverinfo='none',
)


data = [trace1, trace2]
layout = go.Layout(
    title='<b>Top Words in Incident Summaries</b>',
    font=dict(
        family='Raleway, sans-serif'
    ),
    titlefont=dict(
        family='Raleway, sans-serif',
        size=20,
        color='#505C68'),
    showlegend=False,
    xaxis=dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False
    )
)

fig = go.Figure(data=data, layout=layout)

py.plot(fig, filename='middle-east-terrorism-summary-words')