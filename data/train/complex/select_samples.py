import pickle
import json

x = json.load(open('complex_samples.json', encoding='utf-8'))
y = json.load(open('success_examples.json', encoding='utf-8'))

id1, id2 = 0, 0
selected = []

while id1 < len(x) and id2 < len(y):
    if x[id1]['gold'] == y[id2]['g_str'][0] and x[id1]['predict'] == y[id2]['p_str']:
        selected.append(x[id1])
        id1 += 1
        id2 += 1
    else:
        id1 += 1
json.dump(selected, open('true_samples.json', 'w'))

