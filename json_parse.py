import json


#with open('data.txt') as json_file:
#    data = json.load(json_file)
#    for p in data['people']:
#        print('Name: ' + p['name'])
#        print('Website: ' + p['website'])
#        print('From: ' + p['from'])
#        print('')

with open('pipes.json') as json_file:
    data = json.load(json_file)
    print('_id: ' + data['_id'])
    print('')
