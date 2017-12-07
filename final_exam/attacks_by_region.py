import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Read in csv with data
attacks_region_year = pd.read_csv('terrorism_attacks_region_year.csv')

# Get list of regions
regions = pd.unique(attacks_region_year['Region'])

# Get list of years
years = pd.unique(attacks_region_year['Year'])

# Put list of values for each year for each energy source into a dictionary as numpy arrays
region_dict = {}

for region in regions:
    region_subset = attacks_region_year.loc[attacks_region_year['Region'] == region]
    region_dict[region] = np.asarray(region_subset['Count'])

# Create cumulative stacked values
regions_stacked_vals = {}

cum_val = np.zeros(len(years))

for i in range(len(regions)):
    regions_stacked_vals[i] = cum_val + region_dict[regions[i]]
    cum_val = regions_stacked_vals[i]

l = []
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, 13)][:12]

for i in range(len(regions)):
    trace0 = go.Scatter(
        x=years,
        y=regions_stacked_vals[i],
        name=regions[i],
        text=np.asarray([regions[i] + ': ' + format(num, ',d') + ' Incidents'
                         for num in region_dict[regions[i]].astype(int)]),
        hoverinfo='x+text',
        mode='lines',
        line=dict(width=0.5,
                  color=c[i]),
        fill='tonexty'
        )
    l.append(trace0)

layout = go.Layout(
    title='Terrorism Incidents by Region and Year (1970 - 2016)',
    titlefont=dict(
        family='Raleway, sans-serif',
        size=32,
        color='#505C68'),
    xaxis=dict(
        title='Year',
        titlefont=dict(
            family='Raleway, sans-serif'),
        tickfont=dict(
            family='Raleway, sans-serif')
    ),
    yaxis=dict(
        title='Incidents',
        titlefont=dict(
            family='Raleway, sans-serif'),
        tickfont=dict(
            family='Raleway, sans-serif')
    ),
    hoverlabel=dict(
        font=dict(
            family='Raleway, sans-serif')
    ),
    legend=dict(
        font=dict(
            family='Raleway, sans-serif')
    )
)

fig = go.Figure(data=l, layout=layout)
py.iplot(fig, filename='terrorism-incidents-by-region-stacked')
