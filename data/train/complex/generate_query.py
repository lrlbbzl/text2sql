import json

prompt = """## Tables:
{}

## Foreign_keys:
{}

## Query:
{}

Let's think step by step."""
x = json.load(open('false_samples.json', 'r'))
while True:
    idx = int(input())
    s = x[idx]
    a = s['fields'].strip()
    b = s['foreign_keys'].strip()
    b = b[len('Foreign_keys = ') :]
    c = s['question']
    print(prompt.format(a, b, c))
    print()
