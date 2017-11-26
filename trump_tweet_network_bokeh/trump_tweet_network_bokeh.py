# Libraries
import pandas as pd
import re
import networkx as nx
import community
import numpy as np
import operator
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

# Get a list of all of Trump's tweets
tweets = pd.read_csv('trump_tweets_nov2016_oct2017.csv')
non_retweets = tweets[tweets['is_retweet'] == False]
tweet_text = list(non_retweets['text'])

# Create empty data frame for storing edges
edge_list = pd.DataFrame(columns=['from', 'to'])

# Loop through and extract the set of hashtags and mentions in the tweets
# Add each pair (if there are more than one) to an edge list
for tweet in tweet_text:
    hts_mentions = re.findall(r"(@\w+)", tweet)
    if len(hts_mentions) > 1:
        for i in range(len(hts_mentions)-1):
            for j in range(i+1, len(hts_mentions)):
                w1 = hts_mentions[i]
                w2 = hts_mentions[j]
                pair = {'from': sorted([w1, w2])[0],
                        'to': sorted([w1, w2])[1]}
                edge_list = edge_list.append(pair, ignore_index=True)

# Create data frame with edge weights
edge_list = edge_list.groupby(['from', 'to']).size().reset_index(name='weight')

# Get list of vertices
vertices = edge_list['from'].append(edge_list['to']).unique()

# Convert dataframe to a list of tuples
edge_list_tuples = list(edge_list.itertuples(index=False, name=None))

# Create Networkx Graph
G = nx.Graph()
G.add_weighted_edges_from(edge_list_tuples)

# Find number of nodes connected to each vertex
num_neighbors = [len(G.neighbors(v)) for v in vertices]
num_neighbors_dict = {}
for i in range(len(vertices)):
    num_neighbors_dict[vertices[i]] = num_neighbors[i]

# Create smaller edge list
edge_list_subset = [item for item in edge_list_tuples if num_neighbors_dict[item[0]] > 1
                    and num_neighbors_dict[item[1]] > 1]

# Create smaller graph
H = nx.Graph()
H.add_weighted_edges_from(edge_list_subset)

# Get new list of vertices -- which have more than 1 neighbor
vertices_subset = [vertex for vertex in vertices if num_neighbors_dict[vertex] > 1]

# Partition by community
partition = community.best_partition(H)

# Get betweenness and degree of each node
betweenness = nx.betweenness_centrality(H)
degree = nx.degree(H)

# Get a list of vertices sorted by community & associated list of communities
# Also get node degree and betweenness
vertices_partitioned = sorted(partition.items(), key=operator.itemgetter(1))
nodes = [tup[0] for tup in vertices_partitioned]
communities = [tup[1] for tup in vertices_partitioned]
node_betweenness = [betweenness[node] for node in nodes]
node_degree = [degree[node] for node in nodes]

# Create vertex dataframe and save to csv
vertex_df = pd.DataFrame({'ID': nodes,
                          'Group': communities,
                          'nodeDegree': node_betweenness,
                          'nodeBetweenness': node_degree})
vertex_df = vertex_df[['ID', 'Group', 'nodeBetweenness', 'nodeDegree']]
vertex_df.to_csv('nodes.csv', index=False)

# Create dataframe from edge list subset & save to csv
edges_df = pd.DataFrame(edge_list_subset, columns=['From', 'To', 'Weight'])

N = len(nodes)
node_num_dict = {}
for i in range(N):
    node_num_dict[nodes[i]] = i

edges_df['SourceID'] = [node_num_dict[node] for node in edges_df['From']]
edges_df['TargetID'] = [node_num_dict[node] for node in edges_df['To']]

edges_df.to_csv('edges.csv', index=False)

# Set up for plotting
counts = np.zeros((N, N))
for edge in edge_list_subset:
    counts[node_num_dict[edge[0]], node_num_dict[edge[1]]] = edge[2]
    counts[node_num_dict[edge[1]], node_num_dict[edge[0]]] = edge[2]

# Make colormap
colormap = np.asarray(['hsl('+str(h)+',80%'+',40%)' for h in np.linspace(0, 360, 13)])[[0, 2, 4, 6, 8, 10, 1, 3, 5, 7, 9, 11]].tolist()

# Create plot
xname = []
for node in nodes:
    xname += [node]*len(nodes)
yname = nodes*len(nodes)
color = []
alpha = []
for i, node1 in enumerate(nodes):
    for j, node2 in enumerate(nodes):

        alpha.append(min(counts[i, j]/4.0, 0.9) + 0.1)

        if partition[node1] == partition[node2]:
            color.append(colormap[partition[node1]])
        else:
            color.append('lightgrey')

source = ColumnDataSource(data=dict(
    xname=xname,
    yname=yname,
    colors=color,
    alphas=alpha,
    count=counts.flatten(),
))

p = figure(title="Trump Tweet Network",
           x_axis_location="above", tools="hover,save,box_zoom,wheel_zoom,pan,reset",
           x_range=list(reversed(nodes)), y_range=nodes)

p.plot_width = 1000
p.plot_height = 1000
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "6pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

p.rect('xname', 'yname', 0.9, 0.9, source=source,
       color='colors', alpha='alphas', line_color=None,
       hover_line_color='black', hover_color='colors')

p.select_one(HoverTool).tooltips = [
    ('nodes', '@yname, @xname'),
    ('count', '@count'),
]

output_file("trump_tweet_network.html", title="Trump Tweet Network")

show(p)
