from networkx import random_geometric_graph, set_node_attributes, betweenness_centrality
from pyd3netviz import ForceChart
import numpy as np

G=random_geometric_graph(100,0.125)

for u, v in G.edges():
    G[u][v]['link_color'] = '#{}{}{}'.format(np.random.randint(1,9),
                                             np.random.randint(1,5),
                                             np.random.randint(5,9))
set_node_attributes(G, name='node_color', values='#090')
bb = betweenness_centrality(G)

set_node_attributes(G, name='node_size', values={k:50*np.sqrt(v) for k,v in bb.items()})
fc = ForceChart(G, link_color_field='link_color', charge=-100, link_distance=50,
                node_color_field='node_color', node_radius_field='node_size')
fc.to_notebook('./graph_demo_2.html')
