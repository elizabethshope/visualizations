from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

failures = pd.read_csv('terrorism_failures.csv')


percents = go.Scatter(
    x=failures.year,
    y=failures.fail_percent,
    name='Failure Percent',
    yaxis='y2'
)

counts = go.Scatter(
    x=failures.year,
    y=failures.attacks_failures,
    name='Failure Count'
)

fig = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                          shared_xaxes=True, shared_yaxes=False,
                          vertical_spacing=0.1,
                          subplot_titles=('Percentage of Terrorism Incidents that Failed by Year',
                                          'Count of Failed Terrorism Incidents by Year'))

fig.append_trace(percents, 1, 1)
fig.append_trace(counts, 2, 1)

fig['layout'].update(title='<b>Terrorism Incident Failures</b>',
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
                         title='Percentage of Terrorism<br>Incidents that Failed',
                         titlefont=dict(
                             family='Raleway, sans-serif',
                             size=16),
                         tickfont=dict(
                             family='Raleway, sans-serif',
                             size=14)
                     ),
                     yaxis2=dict(
                         title='Count of Terrorism<br>Incidents that Failed',
                         titlefont=dict(
                             family='Raleway, sans-serif',
                             size=16),
                         tickfont=dict(
                             family='Raleway, sans-serif',
                             size=14)
                     ),
                     )

py.iplot(fig, filename='terrorism-failures')
