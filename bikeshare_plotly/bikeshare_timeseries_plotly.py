import pandas as pd
from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go

# Read in data
q3_2016 = pd.read_csv('../../../Downloads/2016-Q3-cabi-trips-history-data/2016-Q3-Trips-History-Data-1.csv')
q3_2016_2 = pd.read_csv('../../../Downloads/2016-Q3-cabi-trips-history-data/2016-Q3-Trips-History-Data-2.csv')
q1_2017 = pd.read_csv('../../../Downloads/2017-Q1-Trips-History-Data.csv')

# Create function to get hourly counts for a period of time
def get_hour_counts(trips_df, month, days, year):

    # Convert start and end dates to datetimes
    trips_df['Start date'] = trips_df['Start date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M'))

    # Add in start month, date, and hour to df
    trips_df['month'] = trips_df['Start date'].apply(lambda x: x.month)
    trips_df['date'] = trips_df['Start date'].apply(lambda x: x.day)
    trips_df['hour'] = trips_df['Start date'].apply(lambda x: x.hour)

    # Get all rides from the week of July 17-23, 2016 & just keep month, date and hour columns
    trips_subset = trips_df[trips_df['month'] == month]
    trips_subset = trips_subset[trips_subset['date'].isin(days)]
    trips_subset = trips_subset[['month', 'date', 'hour']].reset_index(drop=True)

    hourly_count = trips_subset.groupby(['month', 'date', 'hour']).size()\
        .reset_index(name='count')

    return hourly_count

july_17_23_hour_counts = get_hour_counts(q3_2016, 7, [17, 18, 19, 20, 21, 22, 23], 2016)
sept_11_17_hour_counts = get_hour_counts(q3_2016_2, 9, [11, 12, 13, 14, 15, 16, 17], 2016)
jan_22_28_hour_counts = get_hour_counts(q1_2017, 1, [22, 23, 24, 25, 26, 27, 28], 2017)

# Fill in missing values (because there are 0 rides), sort, and reset indices
jan_22_28_hour_counts = jan_22_28_hour_counts.append({'month': 1, 'date': 24, 'hour': 3, 'count': 0}, ignore_index=True)
jan_22_28_hour_counts = jan_22_28_hour_counts.append({'month': 1, 'date': 25, 'hour': 3, 'count': 0}, ignore_index=True)

jan_22_28_hour_counts = jan_22_28_hour_counts.sort_values(['month', 'date', 'hour'], ascending=[True, True, True]).reset_index(drop = True)


def add_dt(hourly_count, year):
    def compute_dt(row, yr):
        dt_string = '%d/%d/%d %d:00' % (row['month'], row['date'], yr, row['hour'])
        return datetime.strptime(dt_string, '%m/%d/%Y %H:%M')

    hourly_count['datetime'] = hourly_count.apply(compute_dt, args=(year,), axis=1)

    return hourly_count


july_17_23_hour_counts = add_dt(july_17_23_hour_counts, 2016)
sept_11_17_hour_counts = add_dt(sept_11_17_hour_counts, 2016)
jan_22_28_hour_counts = add_dt(jan_22_28_hour_counts, 2017)

# Make plot
trace1 = go.Scatter(x=list(july_17_23_hour_counts['datetime']),
                    y=list(july_17_23_hour_counts['count']),
                    name='July 17-23, 2016')

trace2 = go.Scatter(x=list(july_17_23_hour_counts['datetime']),
                    y=list(sept_11_17_hour_counts['count']),
                    name='Sept 11-17, 2016')

trace3 = go.Scatter(x=list(july_17_23_hour_counts['datetime']),
                    y=list(jan_22_28_hour_counts['count']),
                    name='Jan 22-28, 2017')

data = [trace1, trace2, trace3]

layout = dict(
    title='Capital Bikeshare - Trips Per Hour',
    width=736,
    height=500,
    titlefont=dict(
        family='Raleway, sans-serif',
        size=32,
        color='#505C68'),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1d',
                     step='day',
                     stepmode='backward'),
                dict(count=3,
                     label='3d',
                     step='day',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date',
        tickformat='%a %I %p',
        title='Day & Hour',
        titlefont=dict(
            family='Raleway, sans-serif',
            size=16),
        tickfont=dict(
            family='Raleway, sans-serif',
            size=14)
    ),
    yaxis=dict(
        title='Rides per Hour',
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
py.iplot(fig, filename='bikeshare-hourly-trips-with-slider')

