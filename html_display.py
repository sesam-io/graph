import networkx as nx
from networkx.readwrite import json_graph
#from NetworkxD3 import simpleNetworkx

G = nx.Graph()
H = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
G.add_nodes_from(H)
G.add_edges_from([("A", "B"), ("A", "C"), ("A", "D"), ("A", "J"), ("B", "E"), ("B", "F"),
                  ("C", "G"), ("C", "H"), ("D", "I")])

#print(json_graph.node_link_data(G))


#=====================================================================================================
#=====================================================================================================
#=====================================================================================================
#=====================================================================================================
#=====================================================================================================

import networkx as nx
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas as p
from rpy2.robjects import pandas2ri
pandas2ri.activate()
#import pandas.rpy.common as com

def simpleNetworkx(G):

	ro.r('src = c()')
	ro.r('target =c()')
	ro.r('rdf=data.frame()')

	df = p.DataFrame(data=G.edges())

	df_r = pandas2ri.py2rpy(df)

	ro.globalenv['src'] = df_r[0]
	ro.globalenv['target'] = df_r[1]

	ro.r('rdf=data.frame(src,target)')

	utils = importr('utils')
	utils.chooseCRANmirror(ind=1)


	try:
		networkD3 = importr('networkD3')
	except:
		utils.install_packages('networkD3')
		networkD3 = importr('networkD3')

	try:
		magrittr = importr('magrittr')
	except:
		utils.install_packages('magrittr')
		magrittr = importr('magrittr')


	ro.r('''simpleNetwork(rdf) %>% saveNetwork(file = 'Net.html')''')
	return None


#=====================================================================================================
#=====================================================================================================
#=====================================================================================================
#=====================================================================================================
#=====================================================================================================


simpleNetworkx(G)
