# Imports
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# Read in data
mean_killed = pd.read_csv('terrorism_num_killed.csv')

# Make plot
trace1 = go.Scatter(x=list(mean_killed['iyear']),
                    y=list(mean_killed['nkill']))

data = [trace1]

layout = dict(
    title='<b>People Killed per Year</b>',
    titlefont=dict(
        family='Raleway, sans-serif',
        size=20,
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
        title='Total People Killed per Year',
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
py.iplot(fig, filename='total-people-killed-terrorism-incidents')
