import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (2, 1), (2, 3)])

nx.draw(G,with_labels=True)
plt.savefig("graph.png")
plt.show()
