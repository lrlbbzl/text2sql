import json

x = json.load(open('test_data.json', 'r'))
ls = []

for xx in x:
    if ('group by' in xx['gold'] or 'GROUP BY' in xx['gold']):
         ls.append(xx)

json.dump(ls, open('./count/count.json', 'w'))
