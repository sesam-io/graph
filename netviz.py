#pip install networkx==1.11
from networkx import random_geometric_graph
from pyd3netviz import ForceChart

G=random_geometric_graph(100,0.125)

fc =ForceChart(G,charge=-100,link_distance=50,width=590)
fc.to_notebook('./graph_demo.html')
