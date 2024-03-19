import json

dic = {}

x = json.load(open("../group_type_data.json", 'r'))
y = json.load(open('./group_type_data.json', 'r'))

print('\n'.join(list(set(y['Set operation']) - set(x['Set operations']))))

# for p in x:
#     if p['predict'] not in dic:
#         dic.update({p['predict'] : []})
#     else:
#         dic[p['predict']].append(p['query'])
# json.dump(dic, open('group_type_data.json', 'w'))

# # for k, v in x.items():
# #     print('{}: {}'.format(k, len(v)))