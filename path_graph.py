import networkx as nx
import matplotlib.pyplot as plt

G = nx.path_graph(4)
cities = {0: "Toronto", 1: "London", 2: "Berlin", 3: "New York"}

H = nx.relabel_nodes(G, cities)

G.add_nodes_from([('a',{'color':'red'}),'b',('c',{'color':'red'})])

G.add_nodes_from(['a','c'],group=1)
G.add_nodes_from(['b'],group=2)


print("Nodes of graph: ")
print(H.nodes())
print("Edges of graph: ")
print(H.edges())
#nx.draw(H, with_labels=True)
nx.draw(G, with_labels=True, node_color=)
plt.savefig("path_graph_cities.png")
plt.show()
