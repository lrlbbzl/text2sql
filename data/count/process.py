import json

x = json.load(open("predict.json", 'r'))

ls = []

for xx in x:
    xx['predict'] = xx['predict'].replace('\n', '')
    ls.append(xx)
json.dump(ls, open('new.json', 'w'))