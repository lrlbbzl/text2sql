import json

prompt = """## Tables:
{}

## Foreign_keys:
{}

## Query:
{}

Let's think step by step."""
x = json.load(open('test_data.json', 'r'))
y = open('./complex/complex_new.txt', 'r').readlines()


ls = []
for query in y:
    query = query.strip()
    idx = 0
    tep = None
    for i, k in enumerate(x):
        if k['question'] == query:
            tep = k
            break
    ls.append(tep)
json.dump(ls, open('complex_new.json', 'w'))
