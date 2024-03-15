import json 
import pandas as pd
import time
import openai
import os
import sys
import argparse
from tqdm import tqdm

from complex import complex_prompt


API_KEY = 'sk-SWjitJIKQYbpwPyUEDMcyFxRI0Q1fSwnc6mkiOW5AK7tEwxh'
os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://api.chatanywhere.com.cn/v1"
OPENAI_MODEL = 'gpt-3.5-turbo'

reasoning_generate_prompt = complex_prompt


def GPT_generation(prompt):
  response = openai.ChatCompletion.create(
    model=OPENAI_MODEL,
    messages=[{"role": "user", "content": prompt}],
    n = 1,
    stream = False,
    temperature=0.0,
    max_tokens=500,
    top_p = 1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop = ["Q:"]
  )
  return response['choices'][0]['message']['content']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-data", default='./data/complex/complex.json', type=str)
    parser.add_argument("--output-file", default='complex_with_reasoning.json', type=str)
    parser.add_argument("--generate-sql", action='store_true')
    args = parser.parse_args()


    if args.generate_sql:
        output_dir = os.path.dirname(args.test_data)
        data = json.load(open(args.test_data, 'r'))
        new_data = []
        for x in tqdm(data):
            foreign_keys = x['foreign_keys']
            foreign_keys = foreign_keys[foreign_keys.find('Foreign_keys = ') + len('Foreign_keys = ') : ]
            query = complex_prompt.format(x['tables'], foreign_keys, x['question'])
            response = None
            while response is None:
                try:
                    response = GPT_generation(query)
                except:
                    time.sleep(2)
            sql = response.rfind('SQL query: \n')
            ans = response[sql + len('SQL query: \n') :]
            reason = response[:sql]
            x.update({'reasoning' : reason, 'predict' : ans})
            new_data.append(x)
        json.dump(new_data, open(os.path.join(output_dir, 'predict.json'), 'w'))
            