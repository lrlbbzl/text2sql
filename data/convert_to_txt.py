import json
import os

predict_path = './count/predict.json'
x = json.load(open(predict_path, 'r'))
fp1, fp2 = open(os.path.join(os.path.dirname(predict_path), 'dev_gold.txt'), 'w'), open(os.path.join(os.path.dirname(predict_path), 'predicted_sql.txt'), 'w')

ls1, ls2 = [], []

for xx in x:
    ls1.append('{}\t{}'.format(xx['gold'], xx['db_id']))
    pred = xx['predict']
    ls2.append(pred)

fp1.writelines('\n'.join(ls1))
fp2.writelines('\n'.join(ls2))

fp1.close()
fp2.close()
