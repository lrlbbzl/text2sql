import json

files = ['./count/count.json', './complex/complex.json']

output = './others/others.json'
golds = []
for file in files:
    for x in json.load(open(file, 'r')):
        golds.append(x['gold'])

ls = []
for x in json.load(open('./all/test_data.json')):
    if x['gold'] not in golds:
        ls.append(x)

json.dump(ls, open('./others/others.json', 'w'))
