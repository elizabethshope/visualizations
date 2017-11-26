# Imports
import pandas as pd
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Range1d#, BoxZoomTool, ResetTool, PanTool
from bokeh.plotting import figure
import numpy as np

# Set output file
output_file('amazon_reviews_bokeh.html')

# Read in review data
amazon_reviews = pd.read_csv('Amazon_Reviews_Star_Fractions.csv')

# Change order of columns
amazon_reviews = amazon_reviews[['ratings', 'Clothing Shoes and Jewelry', 'Home and Kitchen',
                                 'Electronics', 'Video Games', 'Amazon Instant Video', 'Digital Music']]

# Turn into x values (ratings), y values (percentages) and product categories -- all in the same order
x = [1]*6 + [2]*6 + [3]*6 + [4]*6 + [5]*6
y = list(amazon_reviews.loc[0,][1:]) + list(amazon_reviews.loc[1,][1:]) + list(amazon_reviews.loc[2,][1:]) +\
    list(amazon_reviews.loc[3,][1:]) + list(amazon_reviews.loc[4,][1:])
categories = amazon_reviews.columns.values.tolist()[1:]*5
colors = ['#E11F27', '#3B7FB6', '#51AE4F', '#9751A1', '#FD7F23', '#A4562E']*5


# Create data source for plotting
source = ColumnDataSource(data=dict(
    x=x,
    y=y,
    categories=categories,
    cols=colors,
))

hover = HoverTool(tooltips=[
    ("Star Rating", "@x"),
    ("Fraction of Reviews in Category with Rating", "@y"),
    ("Category", "@categories")
])

p = figure(plot_height=600, plot_width=400,
           title="Amazon Star Rating Fractions by Product Category",
           tools=[hover, 'pan, box_zoom, reset'])

p.circle('x', 'y', size=10, fill_color='cols', fill_alpha=0.3, line_color='cols', line_width=2,
         legend='categories', source=source)

p.legend.location = "top_left"
p.legend.border_line_width = 1
p.legend.border_line_color = "black"
p.legend.border_line_alpha = 0.5
p.y_range = Range1d(0, 1)
p.xaxis.axis_label = 'Star Rating'
p.yaxis.axis_label = 'Fraction of Reviews in Category with Star Rating'

show(p)
