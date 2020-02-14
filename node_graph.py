import networkx as nx
import matplotlib.pyplot as plt
import json

G = nx.DiGraph()
Giso = nx.Graph()

def getKey(item):
    return item[1]

datasets = []
pipes = []

with open('datasets.json') as json_file:
    datasets_json = json.load(json_file)
    for dataset in datasets_json:
        if dataset['runtime']['origin'] != 'system':
            datasets.append(dataset['_id'])

with open('pipes.json') as json_file:
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
                tuple = ds, pipe['config']['effective']['sink']['dataset']
                pipes.append(tuple)
        #outside to dataset
        if pipe['config']['effective']['source']['type'] == 'json' and \
            pipe['config']['effective']['sink']['type'] == 'dataset':
            datasets.append(pipe['_id'] + '_json')
            tuple = pipe['_id'] + '_json', pipe['config']['effective']['sink']['dataset']
            pipes.append(tuple)
        #dataset to outside
        if pipe['config']['effective']['source']['type'] == 'dataset' and \
            pipe['config']['effective']['sink']['type'] == 'json':
            datasets.append(pipe['_id'] + '_json')
            tuple = pipe['config']['effective']['source']['dataset'], pipe['_id'] + '_json'
            pipes.append(tuple)
        #dataset to outside
        if pipe['config']['effective']['source']['type'] == 'dataset' and \
            pipe['config']['effective']['sink']['type'] == 'csv_endpoint':
            datasets.append(pipe['_id'] + '_csv')
            tuple = pipe['config']['effective']['source']['dataset'], pipe['_id'] + '_csv'
            pipes.append(tuple)
        #sql to csv
        if pipe['config']['effective']['source']['type'] == 'sql' and \
            pipe['config']['effective']['sink']['type'] == 'csv_endpoint':
            datasets.append(pipe['_id'] + '_sql')
            datasets.append(pipe['_id'] + '_csv')
            tuple = pipe['_id'] + '_sql', pipe['_id'] + '_csv'
            pipes.append(tuple)

G.add_nodes_from(datasets)
G.add_edges_from(pipes)

isolates = list(nx.isolates(G))

G.remove_nodes_from(isolates)
Giso.add_nodes_from(isolates)

print('=============================')
print('isolates:')
for node in isolates:
    print(node)
print('=============================')
print('10 highest degree of connectivity')
degree = nx.degree(G)

for idx, node in enumerate(sorted(degree, key=getKey, reverse=True)):
    print(node)
    if(idx+1) % 10 == 0:
        break
print('=============================')

print('10 highest degree of centrality')
degree_centrality = nx.degree_centrality(G)
print(degree_centrality)

for idx, node in enumerate(sorted(degree_centrality, key=getKey, reverse=True)):
    print(node + ' ' + getKey(node))
    if(idx+1) % 10 == 0:
        break

print('=============================')
degree_histogram = nx.degree_histogram(G)
plt.figure(1)
plt.plot(degree_histogram)
plt.title('degree of connectivity histogram (curve)')
plt.xlabel('degree of connectivity')
plt.ylabel('# of nodes')
plt.axis([0,sorted(degree, key=getKey, reverse=True)[0][1],0,len(degree)])

plt.figure(2)

if 1:
    nx.draw(G, with_labels=True, pos=nx.spring_layout(G))
else:
    nx.draw(Giso, with_labels=True)

plt.savefig("graph.png")

plt.show()
