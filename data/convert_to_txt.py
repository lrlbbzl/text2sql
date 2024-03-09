import json

x = json.load(open('./predict.json', 'r'))
fp1, fp2 = open('dev_gold.txt', 'w'), open('predicted_sql.txt', 'w')

ls1, ls2 = [], []

for xx in x:
    ls1.append('{}\t{}'.format(xx['gold'], xx['db_id']))
    pred = xx['predict']
    pred = pred[len('SQL query: ') : ]
    ls2.append(pred)

fp1.writelines('\n'.join(ls1))
fp2.writelines('\n'.join(ls2))

fp1.close()
fp2.close()
