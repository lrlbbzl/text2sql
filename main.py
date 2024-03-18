import json 
import pandas as pd
import time
import openai
import os
import sys
import argparse
from tqdm import tqdm

from complex import complex_prompt, complex_search_prompt
from count import count_prompt

from matching import auto_prompting

shot_prompt = """## Tables:
{}

## Foreign_keys:
{}

## Query:
{}

Let's think step by step.

{}
"""

single_prompt = """## Tables:
{}

## Foreign_keys:
{}

## Query:
{}
"""


API_KEY = 'sk-SWjitJIKQYbpwPyUEDMcyFxRI0Q1fSwnc6mkiOW5AK7tEwxh'
os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://api.chatanywhere.com.cn/v1"
OPENAI_MODEL = 'gpt-3.5-turbo'

generate_prompt = count_prompt


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

def generate_single_prompt(x):
    foreign_keys = x['foreign_keys']
    foreign_keys = foreign_keys[foreign_keys.find('Foreign_keys = ') + len('Foreign_keys = ') : ]
    if 'fields' in x:
      return shot_prompt.format(x['fields'], foreign_keys, x['question'], x['reasoning'])
    return single_prompt.format(x['tables'], foreign_keys, x['question'])

def question_to_item(x, data):
   for xx in data:
      if xx['question'] == x:
         return xx

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-data", default='./classification/complex/complex_new.json', type=str)
    parser.add_argument("--train-data", default='./data/train/complex/true_samples.json', type=str)
    args = parser.parse_args()


    output_dir = os.path.join(os.path.dirname(args.test_data), 'auto_select')
    test_data = json.load(open(args.test_data, 'r'))
    train_data = json.load(open(args.train_data, 'r'))
    new_data = []
    # for x in tqdm(data):
        # foreign_keys = x['foreign_keys']
        # foreign_keys = foreign_keys[foreign_keys.find('Foreign_keys = ') + len('Foreign_keys = ') : ]
    #     query = generate_prompt.format(x['tables'], foreign_keys, x['question'])
        # response = None
        # while response is None:
        #     try:
        #         response = GPT_generation(query)
        #     except:
        #         time.sleep(2)
        # time.sleep(2)
        # sql = response.rfind('SQL query: \n')
        # ans = response[sql + len('SQL query: \n') :]
        # reason = response[:sql]
        # x.update({'reasoning' : reason, 'predict' : ans})
        # new_data.append(x)
    # json.dump(new_data, open(os.path.join(output_dir, 'predict.json'), 'w'))
    matching_list = auto_prompting(test_data, train_data)
    for i, (k, v) in tqdm(enumerate(matching_list.items())):
      test_sample = generate_single_prompt(question_to_item(k, test_data))
      train_samples = [generate_single_prompt(question_to_item(v[i], train_data)) for i in range(len(v))]
      final_prompt = complex_search_prompt.format(train_samples[0], train_samples[1], train_samples[2], train_samples[3], test_sample)
      response = None
      while response is None:
        try:
            response = GPT_generation(final_prompt)
        except openai.error.InvalidRequestError:
            temp = question_to_item(k, test_data)
            foreign_keys = temp['foreign_keys']
            response = None
            foreign_keys = foreign_keys[foreign_keys.find('Foreign_keys = ') + len('Foreign_keys = ') : ]
            final_prompt = complex_prompt.format(temp['tables'], foreign_keys, temp['question'])
      sql = response.rfind('SQL query: \n')
      ans = response[sql + len('SQL query: \n') :]
      reason = response[:sql]
      temp = test_data[i]
      temp.update({'reasoning' : reason, 'predict' : ans})
      new_data.append(temp)
    json.dump(new_data, open(os.path.join(output_dir, 'predict.json'), 'w'))