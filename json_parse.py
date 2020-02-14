import json


#with open('data.txt') as json_file:
#    data = json.load(json_file)
#    for p in data['people']:
#        print('Name: ' + p['name'])
#        print('Website: ' + p['website'])
#        print('From: ' + p['from'])
#        print('')

with open('pipes.json') as json_file:
    pipes_json = json.load(json_file)
    for pipe in pipes_json:
        print('_id: ' + pipe['_id'])
        print('source type: ' + pipe['config']['effective']['source']['type'])
        print('target type: ' + pipe['config']['effective']['sink']['type'])
        print('')

if 0:
    with open('datasets.json') as json_file:
        datasets = json.load(json_file)
        for dataset in datasets:
            if dataset['runtime']['origin'] != 'system':
                print('User dataset: ' + dataset['_id'])
                print('')
