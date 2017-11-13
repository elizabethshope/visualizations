import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Read in csv with data
energy_gen = pd.read_csv('energy_generation_by_source_year.csv')

# Get list of energy sources
energy_sources = pd.unique(energy_gen['ENERGY SOURCE'])
energy_sources = energy_sources[[10, 9, 8, 5, 4, 3, 2, 0]]

# Get list of years
years = pd.unique(energy_gen['YEAR'])

# Put list of values for each year for each energy source into a dictionary as numpy arrays
energy_gen_dict = {}

for source in energy_sources:
    if source == 'Other':
        energy_gen_dict[source] = np.asarray(energy_gen.loc[energy_gen['ENERGY SOURCE'] == 'Other']['GENERATION (Megawatthours)']) + \
                                  np.asarray(energy_gen.loc[energy_gen['ENERGY SOURCE'] == 'Other Biomass']['GENERATION (Megawatthours)']) + \
                                  np.asarray(energy_gen.loc[energy_gen['ENERGY SOURCE'] == 'Other Gases']['GENERATION (Megawatthours)']) + \
                                  np.asarray(energy_gen.loc[energy_gen['ENERGY SOURCE'] == 'Geothermal']['GENERATION (Megawatthours)']) + \
                                  np.asarray(energy_gen.loc[energy_gen['ENERGY SOURCE'] == 'Wood and Wood Derived Fuels']['GENERATION (Megawatthours)'])
    else:
        source_subset = energy_gen.loc[energy_gen['ENERGY SOURCE'] == source]
        energy_gen_dict[source] = np.asarray(source_subset['GENERATION (Megawatthours)'])

# Create cumulative stacked values
energy_stacked_vals = {}

cum_val = np.zeros(26)

for i in range(len(energy_sources)):
    energy_stacked_vals[i] = cum_val + energy_gen_dict[energy_sources[i]]
    cum_val = energy_stacked_vals[i]

l = []
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, 9)][:8]

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
    title='Energy Generation by Source in the United States 1990-2015',
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
        title='Energy Generation (Mwh)',
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
py.iplot(fig, filename='stacked-area-plot-hover')
