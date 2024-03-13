import json

x = json.load(open("predict.json", 'r'))

while True:
    ls = input().strip()
    id = 0
    for i, xx in enumerate(x):
        if xx['gold'] == ls:
            id = i
            break   
    print(x[id]['question'])
    print()
    print(x[id]['gold'])
    print()
    print(x[id]['reasoning'])
    print()
    print(x[id]['predict'])