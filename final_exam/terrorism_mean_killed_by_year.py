# Imports
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# Read in data
mean_killed = pd.read_csv('terrorism_mean_killed.csv')

# Make plot
trace1 = go.Scatter(x=list(mean_killed['iyear']),
                    y=list(mean_killed['nkill']))

data = [trace1]

layout = dict(
    title='Average Number of People Killed per Year in Terrorism Incidents 1970-2016',
    titlefont=dict(
        family='Raleway, sans-serif',
        size=32,
        color='#505C68'),
    xaxis=dict(
        rangeslider=dict(),
        title='Year',
        titlefont=dict(
            family='Raleway, sans-serif',
            size=16),
        tickfont=dict(
            family='Raleway, sans-serif',
            size=14)
    ),
    yaxis=dict(
        title='Mean Number of People Killed',
        titlefont=dict(
            family='Raleway, sans-serif',
            size=16),
        tickfont=dict(
            family='Raleway, sans-serif',
            size=14)
    ),
    legend=dict(
        font=dict(
            family='Raleway, sans-serif',
            size=14)
    )
)

fig = dict(data=data, layout=layout)
py.iplot(fig, filename='mean-people-killed-terrorism-incidents')
