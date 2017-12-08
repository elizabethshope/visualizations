# Imports
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# Read in data
ki = pd.read_csv('terrorism_killed_injured.csv')
hover_text = ['<b>Country:</b> %s<br><b>Year:</b> %d<br><b>Number Killed:</b> %d<br><b>Number Injured:</b> %d' %
              (country, year, nkill, nwound) for country, year, nkill, nwound in
              zip(ki.country_txt, ki.iyear, ki.nkill, ki.nwound)]

trace = go.Scattergl(
    x=ki.nwound,
    y=ki.nkill,
    mode='markers',
    text=hover_text,
    hoverinfo='text',
    marker=dict(
        size=10,
        color='rgba(255, 182, 193, .9)',
        line=dict(
            width=2,
        )
    )
)

data = [trace]

layout = go.Layout(
    title='<b>Killed vs. Wounded Across Years and States</b>',
    titlefont=dict(
        family='Raleway, sans-serif',
        size=20,
        color='#505C68'),
    hovermode='closest',
    hoverlabel=dict(
        font=dict(
            family='Raleway, sans-serif')
    ),
    xaxis=dict(
        title='Number of People Wounded',
        titlefont=dict(
            family='Raleway, sans-serif'),
        tickfont=dict(
            family='Raleway, sans-serif')
    ),
    yaxis=dict(
        title='Number of People Killed',
        titlefont=dict(
            family='Raleway, sans-serif'),
        tickfont=dict(
            family='Raleway, sans-serif')
    ),
    showlegend=False
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='killed-wounded-scatter')

