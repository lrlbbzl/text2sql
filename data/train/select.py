import json

words = ['intersect', 'union', 'except', 'group by']

x = json.load(open('train_data.json', 'r'))
ls = []
for p in x:
    label = False
    for w in words:
        if w in p['gold'].lower():
            label = True
            break
    if not label:
        if 'order by' in p['gold'].lower() or 'where' in p['gold'].lower():
            ls.append(p)
json.dump(ls, open('./filter/filter.json', 'w'))