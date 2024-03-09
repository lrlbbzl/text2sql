import json

x = json.load(open("test_data.json", 'r'))
xx = []
key = ['intersect', 'INTERSECT', 'UNION', 'union', 'EXCEPT', 'except']

for t in x:
    flag = False
    for k in key:
        if k in t['gold']:
            flag = True
            break
    if flag:
        xx.append(t)
    
json.dump(xx, open("complex.json", 'w'))
