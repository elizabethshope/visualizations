import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Read in csv with data
energy_gen = pd.read_csv('energy_generation_by_source_year.csv')

# Get list of energy sources
energy_sources = pd.unique(energy_gen['ENERGY SOURCE'])
energy_sources = energy_sources[[11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]

# Get list of years
years = pd.unique(energy_gen['YEAR'])

# Put list of values for each year for each energy source into a dictionary as numpy arrays
energy_gen_dict = {}

for source in energy_sources:
    source_subset = energy_gen.loc[energy_gen['ENERGY SOURCE'] == source]
    energy_gen_dict[source] = np.asarray(source_subset['GENERATION (Megawatthours)'])

# Create cumulative stacked values
energy_stacked_vals = {}

cum_val = np.zeros(26)

for i in range(len(energy_sources)):
    energy_stacked_vals[i] = cum_val + energy_gen_dict[energy_sources[i]]
    cum_val = energy_stacked_vals[i]

l = []
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(10, 370, 13)][:12]

for i in range(len(energy_sources)):
    trace0 = go.Scatter(
        x=years,
        y=energy_stacked_vals[i],
        name=energy_sources[i],
        text=np.asarray([energy_sources[i] + ': ' + format(num, ',d') + ' Mwh'
                         for num in energy_gen_dict[energy_sources[i]].astype(int)]),
        hoverinfo='x+text',
        mode='lines',
        line=dict(width=0.5,
                  color=c[i]),
        fill='tonexty'
        )
    l.append(trace0)

layout = go.Layout(
    title='<b>Energy Generation by Source in the United States 1990-2015</b>',
    titlefont=dict(
        size=18,
    ),
    xaxis=dict(
        title='Year',
    ),
    yaxis=dict(
        title='Energy Generation (Mwh)',
    ),
)

fig = go.Figure(data=l, layout=layout)
py.iplot(fig, filename='stacked-area-plot-hover')
