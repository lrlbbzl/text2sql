import json

x = json.load(open("./filter.json", 'r'))
y = json.load(open('../../../Few-shot-NL2SQL-with-prompting/outputs/fail_examples.json', 'r'))

temp = [p['g_str'][0] for p in y]
ls = []
for p in x:
    if p['gold'] in temp:
        ls.append(p)
json.dump(ls, open('fail_filter.json', 'w'))
print(len(ls))