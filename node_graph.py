import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import json
from networkx.readwrite import json_graph
from pyd3netviz import ForceChart
import numpy as np

G = nx.DiGraph()
Giso = nx.Graph()

display_metrics = True
output_graph = False
plot_graph = True
list_nodes = False
html_graph = True
show_histo = False

print('\n\n\nUsing networkx version: ' + nx.__version__ + '\n\n\n')

def getKey(item):
    return item[1]

datasets = []
pipes = []
pairs = []

with open('datasets2.json') as json_file:
    datasets_json = json.load(json_file)
    for dataset in datasets_json:
        if dataset['runtime']['origin'] != 'system':
            datasets.append(dataset['_id'])

with open('pipes2.json') as json_file:
    pipes_json = json.load(json_file)
    for pipe in pipes_json:
        #embedded to dataset
        if pipe['config']['effective']['source']['type'] == 'embedded' and \
                pipe['config']['effective']['sink']['type'] == 'dataset':
            datasets.append('embedded_data_' + pipe['_id'])
            tuple = 'embedded_data_' + pipe['_id'], pipe['config']['effective']['sink']['dataset']
            pipes.append(tuple)
        #dataset to dataset
        if pipe['config']['effective']['source']['type'] == 'dataset' and \
            pipe['config']['effective']['sink']['type'] == 'dataset':
            tuple = pipe['config']['effective']['source']['dataset'] , pipe['config']['effective']['sink']['dataset']
            pipes.append(tuple)
        #merge pipes
        if pipe['config']['effective']['source']['type'] == 'merge' and \
            pipe['config']['effective']['sink']['type'] == 'dataset':
            for ds in pipe['config']['effective']['source']['datasets']:
                tuple = ds.split()[0], pipe['config']['effective']['sink']['dataset']
                pipes.append(tuple)
        #outside to dataset
        if (pipe['config']['effective']['source']['type'] == 'json' or pipe['config']['effective']['source']['type'] == 'http_endpoint') and \
                pipe['config']['effective']['sink']['type'] == 'dataset':
            if pipe['config']['effective']['source']['system'] not in datasets:
                datasets.append(pipe['config']['effective']['source']['system'])
                set_node_attributes(G, name='node_color', values='#090')
            tuple = pipe['config']['effective']['source']['system'], pipe['config']['effective']['sink']['dataset']
            pipes.append(tuple)
        #outside http to dataset
#        if pipe['config']['effective']['source']['type'] == 'http_endpoint' and \
#            pipe['config']['effective']['sink']['type'] == 'dataset':
#            if pipe['config']['effective']['source']['system'] not in datasets:
#                datasets.append(pipe['config']['effective']['source']['system'])
#            tuple = pipe['config']['effective']['source']['system'], pipe['config']['effective']['sink']['dataset']
#            pipes.append(tuple)
        #dataset to outside
        if pipe['config']['effective']['source']['type'] == 'dataset' and \
            pipe['config']['effective']['sink']['type'] == 'json':
            if pipe['config']['effective']['sink']['system'] not in datasets:
                datasets.append(pipe['config']['effective']['sink']['system'])
            tuple = pipe['config']['effective']['source']['dataset'], pipe['config']['effective']['sink']['system']
            pipes.append(tuple)
        #dataset to outside
        if pipe['config']['effective']['source']['type'] == 'dataset' and \
            pipe['config']['effective']['sink']['type'] == 'csv_endpoint':
            if pipe['config']['effective']['sink']['system'] not in datasets:
                datasets.append(pipe['config']['effective']['sink']['system'])
            tuple = pipe['config']['effective']['source']['dataset'], pipe['config']['effective']['sink']['system']
            pipes.append(tuple)
        #binary to replicate
        if pipe['config']['effective']['source']['type'] == 'binary' and \
            pipe['config']['effective']['sink']['type'] == 'replicated_dataset':
            if pipe['config']['effective']['source']['system'] not in datasets:
                datasets.append(pipe['config']['effective']['source']['system'])
            tuple = pipe['config']['effective']['source']['system'], pipe['config']['effective']['sink']['dataset']
            pipes.append(tuple)
        #binary to dataset
        if pipe['config']['effective']['source']['type'] == 'binary' and \
            pipe['config']['effective']['sink']['type'] == 'dataset':
            if pipe['config']['effective']['source']['system'] not in datasets:
                datasets.append(pipe['config']['effective']['source']['system'])
            tuple = pipe['config']['effective']['source']['system'], pipe['config']['effective']['sink']['dataset']
            pipes.append(tuple)
        #sql to csv
        if pipe['config']['effective']['source']['type'] == 'sql' and \
            pipe['config']['effective']['sink']['type'] == 'csv_endpoint':
            if pipe['config']['effective']['source']['system'] not in datasets:
                datasets.append(pipe['config']['effective']['source']['system'])
            if pipe['config']['effective']['sink']['system'] not in datasets:
                datasets.append(pipe['config']['effective']['sink']['system'])
            tuple = pipe['config']['effective']['source']['system'], pipe['config']['effective']['sink']['system']
            pipes.append(tuple)

G.add_nodes_from(datasets)
G.add_edges_from(pipes)

#print(list(G.nodes(data=True)))
if list_nodes:
    for dataset in datasets:
        print(dataset)
        '''
        if 'embedded_data_' in dataset:
            #nx.set_node_attributes(G,dataset, 'embedded')
            #print('atr: embedded ' + str(dataset))
            #G.nodes[dataset]['location'] = 'embedded'
            G.nodes[dataset]['location'] = 0
        else:
            #nx.set_node_attributes(G,dataset, 'regular')
            #print('atr: regular ' + str(dataset))
            G.nodes[dataset]['location'] = 1
            #G.nodes[dataset]['location'] = 'regular'
    '''
#print(list(G.nodes(data=True)))

#print(list(G.nodes(data='location')))

isolates = list(nx.isolates(G))

G.remove_nodes_from(isolates)
Giso.add_nodes_from(isolates)

#degree of connectivity
degree = nx.degree(G)

#degree of centrality
degree_centrality = nx.degree_centrality(G)

''' remove pairs'''
if (nx.__version__ == "1.11"):
    for node in datasets:
        if G.degree(node) == 1:
            if len(G.in_edges(node)) == 1:
                for neighbor in G.predecessors(node):
                    if G.degree(neighbor) == 1:
                        pairs.append(neighbor)
            elif len(G.out_edges(node)) == 1:
                for neighbor in G.successors(node):
                    if G.degree(neighbor) == 1:
                        pairs.append(neighbor)
else:
    for node in degree:
        if node[1] == 1:
            #print('---------------------------')
            #print(node)
            if len(G.in_edges(node[0])) == 1:
                for edge in G.in_edges(node[0]):
                    if (len(G.in_edges(edge[0])) + len(G.out_edges(edge[0]))) == 1:
                        pairs.append(node[0])
                        #print(str(len(G.in_edges(edge[0])) + len(G.out_edges(edge[0]))) + ' GONE')
                    #else:
                        #print(str(len(G.in_edges(edge[0])) + len(G.out_edges(edge[0]))) + ' DONC NIET')
            else:
                for edge in G.out_edges(node[0]):
                    if (len(G.in_edges(edge[1])) + len(G.out_edges(edge[1]))) == 1:
                        pairs.append(node[0])
                        #print(str(len(G.in_edges(edge[1])) + len(G.out_edges(edge[1]))) + ' GONE')
                    #else:
                        #print(str(len(G.in_edges(edge[1])) + len(G.out_edges(edge[1]))) + ' DONC NIET')
            #for neighbor in G.neighbors(node[0]):
            #print('---------------------------')
            #print('++++++++++++++++++++++++++++')
            #print(str(len(G.in_edges(node[0])) + len(G.out_edges(node[0]))) + ' EN TOUT')
            #print('++++++++++++++++++++++++++++')
            #print(str(len(G.in_edges(node[0]))) + ' IN  ')
            #print(G.in_edges(node[0]))
            #print(str(len(G.out_edges(node[0]))) + ' OUT ')
            #print(G.out_edges(node[0]))
            #print('++++++++++++++++++++++++++++')
            #for edge in G.in_edges(node[0]):
                #print('\t' + 'IN  ' + edge[0])
            #for edge in G.out_edges(node[0]):
                #print('\t' + 'OUT ' + edge[1])
                #pairs.append(node[0])

for node in pairs:
    G.remove_node(node)


if display_metrics and nx.__version__ != "1.11":
    print('=============================')

    print('isolates:')
    for node in isolates:
        print(node)

    print('=============================')

    print('10 highest degree of connectivity')

    for idx, node in enumerate(sorted(degree, key=getKey, reverse=True)):
        print(node[0] + ' ' + str(node[1]))
        if(idx+1) % 10 == 0:
            break

    print('=============================')

    print('10 highest degree of centrality')

    for idx, node in enumerate(sorted(degree, key=getKey, reverse=True)):
        print(node[0] + ' ' + str(degree_centrality[node[0]]))
        if(idx+1) % 10 == 0:
            break

    print('=============================')

    print('neighbors of highest degree of connectivity')

    for idx, node in enumerate(sorted(degree, key=getKey, reverse=True)):
        print(node[0] + ' ' + str(degree_centrality[node[0]]))
        if (idx + 1) % 10 == 0:
            break

#print(str(degree[0]))

#for bor in  G.neighbors(degree[0][0]):

    print('=============================')

if show_histo:
    degree_histogram = nx.degree_histogram(G)
    plt.figure(1).patch.set_facecolor('lightgray')
    ax = plt.axes(yscale='log')
    ax.patch.set_facecolor('lightgray')
    ax.grid()
    plt.title('degree of connectivity histogram (curve)')
    plt.xlabel('degree of connectivity')
    plt.ylabel('# of nodes')
    plt.xticks(np.arange(0.5, 20, step=1))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    plt.ylim(top=math.ceil(max(degree_histogram)/100)*100+(math.ceil(max(degree_histogram)/100)*100/2),bottom=0.7)
    plt.xlim(left=-1,right=len(degree_histogram))
    plt.plot(degree_histogram, color='firebrick')

'''
plt.figure(3)
plt.plot(degree_histogram)
plt.yscale('log')
plt.title('degree of connectivity histogram (curve)')
plt.xlabel('degree of connectivity')
plt.ylabel('# of nodes')
plt.xticks(np.arange(0.5, 20, step=3))
plt.axis([0,sorted(degree, key=getKey, reverse=True)[0][1],0,len(degree)])
'''

if plot_graph:
    if (nx.__version__ != "1.11"):
        plt.figure(2, figsize=(20,13)).patch.set_facecolor('lightgray')

        if 0:
            nx.draw(G, with_labels=True, pos=nx.spring_layout(G))
        else:
            nx.draw(Giso, with_labels=True)

        plt.savefig("graph.png")
    else:
        print('can\'t plot with matplotlib using Networkx version 1.11\n\n\n')

if output_graph:
    print(json_graph.node_link_data(G))

if (html_graph):
    if (nx.__version__ == "1.11"):
        fc = ForceChart(G, default_node_color='green', charge=-100, link_distance=50, height=1500, width=2000)
        fc.to_notebook('./graph_demo.html')
    else:
        print('Networkx version 1.11 required to output force graph')

plt.show()
