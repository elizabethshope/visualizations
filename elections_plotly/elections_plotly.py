import plotly.plotly as py
import pandas as pd

# Read in data
election_results_long = pd.read_csv('election_results_long.csv')

# Cast all rows as strings
for col in election_results_long.columns:
    election_results_long[col] = election_results_long[col].astype(str)

# Determine and add winners
d_percents = election_results_long['dem'].astype(float)
r_percents = election_results_long['rep'].astype(float)
d_gr_r = d_percents > r_percents
election_results_long['winner'] = ['D' if item else 'R' for item in d_gr_r]

# Get sorted list of years
years = election_results_long['year'].unique()
years.sort()

races = ["'96: <b><i>Clinton (D)</i></b> vs. Bush (R)", "'00: Gore (D) vs. <b><i>Bush (R)</i></b>",
         "'04: Kerry (D) vs. <b><i>Bush (R)</i></b>", "'08: <b><i>Obama (D)</i></b> vs. McCain (R)",
         "'12: <b><i>Obama (D)</i></b> vs. Romney (R)", "'16: Clinton (D) vs. <b><i>Trump (R)</i></b>"]

dems = ['Clinton', 'Gore', 'Kerry', 'Obama', 'Obama', 'Clinton']
reps = ['Bush', 'Bush', 'Bush', 'McCain', 'Romney', 'Trump']

data = []

layout = dict(
    title='U.S. Presidential General Elections: Winners by Party, State and Year',
    titlefont=dict(
        family='Raleway, sans-serif',
        size=32,
        color='#505C68'),
    showlegend=False,
    autosize=False,
)

for i in range(len(years)):
    geo_key = 'geo'+str(i+1) if i != 0 else 'geo'
    dem_states = election_results_long[election_results_long['winner'] == 'D']
    rep_states = election_results_long[election_results_long['winner'] == 'R']
    dem_locations = dem_states[dem_states['year'] == years[i]]['code']
    rep_locations = rep_states[rep_states['year'] == years[i]]['code']
    dem_states_year = dem_states[dem_states['year'] == years[i]]
    rep_states_year = rep_states[rep_states['year'] == years[i]]
    dem_text = '<b>' + dem_states_year['state'] + '</b><br>' + \
               dems[i] + ': ' + dem_states_year['dem'] + '%<br>' + \
               reps[i] + ': ' + dem_states_year['rep'] + '%'
    rep_text = '<b>' + rep_states_year['state'] + '</b><br>' + \
               dems[i] + ': ' + rep_states_year['dem'] + '%<br>' + \
               reps[i] + ': ' + rep_states_year['rep'] + '%'
    z_dem = [0]*len(dem_text)
    z_rep = [0]*len(rep_text)

    # Annual map data
    data.append(
        dict(
            type='choropleth',
            colorscale=[[0, 'blue'], [1, 'blue']],
            colorbar=dict(
                len=0.17,
                y=0.98,
                yanchor='top',
                tickvals=[0],
                ticktext=[''],
                title='Democrat Winner',
                titlefont=dict(
                    family='Raleway, sans-serif',
                    size=14)
                ),
            autocolorscale=False,
            locations=dem_locations,
            z=z_dem,
            geo=geo_key,
            locationmode='USA-states',
            text=dem_text,
            hoverinfo='text',
            hoverlabel=dict(
                font=dict(
                    family='Raleway, sans-serif')
            ),
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )
            )
        )
    )

    data.append(
        dict(
            type='choropleth',
            colorscale=[[0, 'red'], [1, 'red']],
            colorbar=dict(
                len=0.17,
                y=0.8,
                yanchor='top',
                tickvals=[0],
                ticktext=[''],
                title='Republican Winner',
                titlefont=dict(
                    family='Raleway, sans-serif',
                    size=14)
            ),
            autocolorscale=False,
            locations=rep_locations,
            z=z_rep,
            geo=geo_key,
            locationmode='USA-states',
            text=rep_text,
            hoverinfo='text',
            hoverlabel=dict(
                font=dict(
                    family='Raleway, sans-serif')
            ),
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )
            )
        )
    )

    # Race markers
    data.append(
        dict(
            type='scattergeo',
            showlegend=False,
            lon=[-92],
            lat=[51],
            geo=geo_key,
            text=[races[i]],
            mode='text',
            hoverinfo='none',
            textfont=dict(
                family='Raleway, sans-serif',
                size=15)
        )
    )

    # Set layout
    layout[geo_key] = dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showland=True,
        showlakes=True,
        landcolor='rgb(229, 229, 229)',
        lakecolor='rgb(255, 255, 255)',
        showcountries=False,
        subunitcolor="rgb(255, 255, 255)",
        domain=dict(x=[], y=[]),
    )

z = 0
COLS = 3
ROWS = 2
for y in reversed(range(ROWS)):
    for x in range(COLS):
        geo_key = 'geo'+str(z+1) if z != 0 else 'geo'
        layout[geo_key]['domain']['x'] = [float(x)/float(COLS), float(x+1)/float(COLS)]
        layout[geo_key]['domain']['y'] = [float(y)/float(ROWS), float(y+1)/float(ROWS)]
        z=z+1
        if z > 5:
            break

fig = {'data':data, 'layout':layout}

py.iplot(fig, filename='Maps: U.S. General Election Results by State')
