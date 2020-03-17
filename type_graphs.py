# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Build a dataframe with your connections
df = pd.DataFrame({'from': ['A', 'B', 'C', 'A'], 'to': ['D', 'A', 'E', 'C']})

# And a data frame with characteristics for your nodes
carac = pd.DataFrame({'ID': ['A', 'B', 'C', 'D', 'E'], 'myvalue': ['group1', 'group1', 'group2', 'group3', 'group3']})

# Build your graph
G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())

# The order of the node for networkX is the following order:
print('============================1')
print(G.nodes())
# Thus, we cannot give directly the 'myvalue' column to netowrkX, we need to arrange the order!

print('============================2')
print(carac)
# Here is the tricky part: I need to reorder carac to assign the good color to each node
carac = carac.set_index('ID')
print('============================3')
print(carac)

carac = carac.reindex(G.nodes())
print('============================4')
print(carac)

# And I need to transform my categorical column in a numerical value: group1->1, group2->2...
carac['myvalue'] = pd.Categorical(carac['myvalue'])
carac['myvalue'].cat.codes

print('============================5')
print(carac['myvalue'].cat.codes)

print('============================6')
print(list(G.nodes(data=True)))


# Custom the nodes:
nx.draw(G, with_labels=True, node_color=carac['myvalue'].cat.codes, cmap=plt.cm.Set1, node_size=1500)

#plt.show()
