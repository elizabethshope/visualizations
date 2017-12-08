from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

suicides = pd.read_csv('terrorism_suicides.csv')


portions = go.Scatter(
    x=suicides.year,
    y=suicides.suicide_portion,
    name='Suicide Portion',
    yaxis='y2'
)

counts = go.Scatter(
    x=suicides.year,
    y=suicides.suicide_count,
    name='Suicide Count'
)

fig = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                          shared_xaxes=True, shared_yaxes=False,
                          vertical_spacing=0.1,
                          subplot_titles=('Portion of Terrorism Incidents that are Suicides by Year',
                                          'Count of Suicide Terrorism Incidents by Year'))

fig.append_trace(portions, 1, 1)
fig.append_trace(counts, 2, 1)

fig['layout'].update(title='<b>Terrorism Incident Suicides</b>',
                     titlefont=dict(
                         family='Raleway, sans-serif',
                         size=20,
                         color='#505C68'),
                     xaxis=dict(
                         title='Year',
                         titlefont=dict(
                             family='Raleway, sans-serif',
                             size=16),
                         tickfont=dict(
                             family='Raleway, sans-serif',
                             size=14),
                         anchor='y2'
                     ),
                     yaxis1=dict(
                         title='Portion of Terrorism Incidents<br>that are Suicides',
                         titlefont=dict(
                             family='Raleway, sans-serif',
                             size=16),
                         tickfont=dict(
                             family='Raleway, sans-serif',
                             size=14)
                     ),
                     yaxis2=dict(
                         title='Count of Suicide<br>Terrorism Incidents',
                         titlefont=dict(
                             family='Raleway, sans-serif',
                             size=16),
                         tickfont=dict(
                             family='Raleway, sans-serif',
                             size=14)
                     ),
                     )

py.iplot(fig, filename='terrorism-suicides')
