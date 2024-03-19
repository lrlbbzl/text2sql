import json

x = json.load(open("group_type_data.json", 'r'))
data = x['Set operation']

complex = json.load(open("complex.json", 'r'))
question = [y['question'] for y in complex]
ls = list(set(question)-set(data))
print('\n'.join(list(set(data) - set(question))))
# print('\n'.join(ls))
print(len(ls))