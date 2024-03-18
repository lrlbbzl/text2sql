import json

x = json.load(open('predict.json', 'r'))

print(x[0]['reasoning'])
print(x[0]['predict'])

ls = []

for xx in x:
    predict = xx['predict']
    sql = predict[predict.rfind('SQL query: ') + len('SQL query: ') :]
    reason = xx['reasoning']
    reason = reason[:reason.rfind('SQL query: ')] + 'SQL query: ' + sql
    xx['reasoning'] = reason
    xx['predict'] = sql
    ls.append(xx)

json.dump(ls, open('temp.json', 'w'))