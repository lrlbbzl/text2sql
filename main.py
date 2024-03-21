import json 
import pandas as pd
import time
import openai
import os
import sys
import argparse
from tqdm import tqdm

from complex import complex_prompt, complex_search_prompt
from combination import combination_prompt, combination_search_prompt
from filter import filter_prompt, filter_search_prompt

from matching import auto_prompting

freeze_prompt = """You are a powerful text-to-SQL reasoner. Currently, I am seeking to transform intricate text queries into analytical statements that simplify the creation of SQL statements, leading to the generation of the final SQL query. Our current focus lies in the category of combination operations. Please learn from the provided examples, design a detailed plan for the text query, and present the resulting SQL query.


Example 1:
## Tables:
Table gymnast, columns = [*,Gymnast_ID,Floor_Exercise_Points,Pommel_Horse_Points,Rings_Points,Vault_Points,Parallel_Bars_Points,Horizontal_Bar_Points,Total_Points]
Table people, columns = [*,People_ID,Name,Age,Height,Hometown]

## Foreign_keys:
[gymnast.Gymnast_ID = people.People_ID]

## Query:
How many gymnasts are from each hometown?

Let's think step by step.

<1> Operation: the query requires the number of gymnasts from each hometown, so we should apply the 'count' operation to table 'gymnast', and it does not need sort. Since the unit to which the gymnasts being counted in the query belong is hometown and only table 'people' has column 'Hometown', so we should apply the 'group by' operation to column 'Hometown' in table 'people'. 

<2> Schema Linking: In this step, we identify the tables and columns that should be used based on the first step and the foreign key relationships. Due to the direct foreign key connection between table 'gymnast' and 'people', we need to use tables ['gymnast', 'people']. 

<3> SQL Generation: The query requires number of gymnasts from each hometown, so we should select the count and 'hometown' in people.

SQL query: SELECT T2.Hometown ,  COUNT(*) FROM gymnast AS T1 JOIN people AS T2 ON T1.Gymnast_ID  =  T2.People_ID GROUP BY T2.Hometown


Example 2:
## Tables:
Table county, columns = [*,County_Id,County_name,Population,Zip_code]
Table election, columns = [*,Election_ID,Counties_Represented,District,Delegate,Party,First_Elected,Committee]
Table party, columns = [*,Party_ID,Year,Party,Governor,Lieutenant_Governor,Comptroller,Attorney_General,US_Senate]

## Foreign_keys
[election.District = county.County_Id,election.Party = party.Party_ID]

## Query:
Show the name of each party and the corresponding number of delegates from that party.

Decompose and find the tables to be used:

Let's think step by step.

<1> Operation: The query requires the name of each party and the corresponding number of delegates from that party, so we should apply the 'count' operation to table 'election' for the 'Delegate' column, and it does not need sorting. Since the unit to which the delegates being counted in the query belong is the party and only table 'party' has the column 'Party', so we should apply the 'group by' operation to column 'Party' in table 'party'.

<2> Schema Linking: In this step, we identify the tables and columns that should be used based on the first step and the foreign key relationships. Due to the direct foreign key connection between table 'election' and 'party'. We need to use tables ['election', 'party'].

<3> SQL Generation: The query requires the name of each party and the corresponding number of delegates from that party, so we should select the 'Party' column in the 'party' table and count the 'Delegate' column in the 'election' table.

SQL query: SELECT T1.Party , COUNT(*) FROM party AS T1 JOIN election AS T2 ON T1.Party_ID = T2.Party GROUP BY T1.Party


Example 3:
## Tables:
Table city, columns = [*,City_ID,Official_Name,Status,Area_km_2,Population,Census_Ranking]
Table competition_record, columns = [*,Competition_ID,Farm_ID,Rank]
Table farm, columns = [*,Farm_ID,Year,Total_Horses,Working_Horses,Total_Cattle,Oxen,Bulls,Cows,Pigs,Sheep_and_Goats]
Table farm_competition, columns = [*,Competition_ID,Year,Theme,Host_city_ID,Hosts]

## Foreign_keys:
[farm_competition.Host_city_ID = city.City_ID,competition_record.Farm_ID = farm.Farm_ID,competition_record.Competition_ID = farm_competition.Competition_ID]

## Query:
Show the status of the city that has hosted the greatest number of competitions.

Decompose and find the tables to be used:

Let's think step by step.

<1> Operation: The query requires the city that has hosted greatest number of competitions, so we should apply the 'count' operation to table 'farm_competition', and sort it in descending order. Since the unit to which the competitions being counted in the query belong is city and only table 'farm_competition' has column 'Host_city_ID', so we should apply the 'group by' operation to column 'Host_city_ID' in table 'farm_competition'.

<2> Schema Linking: In this step, we identify the tables and columns that should be used based on the requirements of the query and the foreign key relationships. Due to the direct foreign key connection between table 'city' and 'farm_competition'. We need to use tables ['city', 'farm_competition'].

<3> SQL generation: The query requires the status of the city that has hosted the greatest number of competitions, so we should select the 'Status' column in the 'city' table. The query does not require the count of most competitions, so it is only used for filtering and not selected. 

SQL query: SELECT T1.Status FROM city AS T1 JOIN farm_competition AS T2 ON T1.City_ID  =  T2.Host_city_ID GROUP BY T2.Host_city_ID ORDER BY COUNT(*) DESC LIMIT 1


Example 4:
## Tables:
Table albums, columns = [*,id,title,artist_id]\nTable artists, columns = [*,id,name]
Table customers, columns = [*,id,first_name,last_name,company,address,city,state,country,postal_code,phone,fax,email,support_rep_id]
Table employees, columns = [*,id,last_name,first_name,title,reports_to,birth_date,hire_date,address,city,state,country,postal_code,phone,fax,email]
Table genres, columns = [*,id,name]
Table invoice_lines, columns = [*,id,invoice_id,track_id,unit_price,quantity]
Table invoices, columns = [*,id,customer_id,invoice_date,billing_address,billing_city,billing_state,billing_country,billing_postal_code,total]
Table media_types, columns = [*,id,name]
Table playlist_tracks, columns = [*,playlist_id,track_id]
Table playlists, columns = [*,id,name]
Table sqlite_sequence, columns = [*,name,seq]
Table tracks, columns = [*,id,name,album_id,media_type_id,genre_id,composer,milliseconds,bytes,unit_price]

## Foreign_keys:
[albums.artist_id = artists.id,employees.reports_to = employees.id,customers.support_rep_id = employees.id,invoices.customer_id = customers.id,tracks.media_type_id = media_types.id,tracks.genre_id = genres.id,tracks.album_id = albums.id,invoice_lines.track_id = tracks.id,invoice_lines.invoice_id = invoices.id,playlist_tracks.track_id = tracks.id,playlist_tracks.playlist_id = playlists.id]

## Query:
A list of the top 10 countries by average invoice size. List country name and average invoice size.

Let's think step by step.

<1> Operation: The query requires the top 10 countries by average invoice size, so we should apply the 'average' operation to the 'total' column in the 'invoices' table and sort it in descending order. Since the unit to which the average invoice size being calculated in the query belongs is the country and only table 'customers' has the column 'country', we should apply the 'group by' operation to the 'country' column in the 'customers' table.

<2> Schema Linking: In this step, we identify the tables and columns that should be used based on the first step and the foreign key relationships. Due to the direct foreign key connection between table 'invoices' and 'customers', we need to use tables ['invoices', 'customers'].

<3> SQL Generation: The query requires the top 10 countries by average invoice size, so we should select the 'country' column in the 'customers' table and the average of the 'total' column in the 'invoices' table.

SQL query: 
SELECT T1.country, AVG(T2.total) FROM customers AS T1 JOIN invoices AS T2 ON T1.id = T2.customer_id GROUP BY T1.country ORDER BY AVG(T2.total) DESC LIMIT 10


Example 5:
## Tables:
Table city, columns = [*,City_ID,Official_Name,Status,Area_km_2,Population,Census_Ranking]
Table competition_record, columns = [*,Competition_ID,Farm_ID,Rank]
Table farm, columns = [*,Farm_ID,Year,Total_Horses,Working_Horses,Total_Cattle,Oxen,Bulls,Cows,Pigs,Sheep_and_Goats]
Table farm_competition, columns = [*,Competition_ID,Year,Theme,Host_city_ID,Hosts]

## Foreign_keys:
[farm_competition.Host_city_ID = city.City_ID,competition_record.Farm_ID = farm.Farm_ID,competition_record.Competition_ID = farm_competition.Competition_ID]

## Query:
Please show the different statuses, ordered by the number of cities that have each.

Let's think step by step.

<1> Operation: The query requires the different statuses ordered by the number of cities that have each status, so we should apply the 'count' operation to the 'city' table for the 'Status' column, and sort it in ascending order. Since the unit to which the statuses being counted in the query belong is the city, we should apply the 'group by' operation to the 'Status' column in the 'city' table.

<2> Schema Linking: In this step, we identify the tables and columns that should be used based on the first step and the foreign key relationships. In this question, we only need to use table ['city'].

<3> SQL Generation: The query requires the different statuses ordered by the number of cities that have each status, so we should select the 'Status' column in the 'city' table. The query does not require the count of cities so it is only used for filtering and not selected. 

SQL query: SELECT Status FROM city GROUP BY Status ORDER BY COUNT(*) ASC


Example 6:
## Tables:
Table station, columns = [*,id,name,lat,long,dock_count,city,installation_date]
Table status, columns = [*,station_id,bikes_available,docks_available,time]
Table trip, columns = [*,id,duration,start_date,start_station_name,start_station_id,end_date,end_station_name,end_station_id,bike_id,subscription_type,zip_code]
Table weather, columns = [*,date,max_temperature_f,mean_temperature_f,min_temperature_f,max_dew_point_f,mean_dew_point_f,min_dew_point_f,max_humidity,mean_humidity,min_humidity,max_sea_level_pressure_inches,mean_sea_level_pressure_inches,min_sea_level_pressure_inches,max_visibility_miles,mean_visibility_miles,min_visibility_miles,max_wind_Speed_mph,mean_wind_speed_mph,max_gust_speed_mph,precipitation_inches,cloud_cover,events,wind_dir_degrees,zip_code]

## Foreign_keys:
[status.station_id = station.id]

## Query:
For each city, list their names in decreasing order by their highest station latitude.

Let's think step by step.

<1> Operation: The query requires the city names in decreasing order by their highest station latitude, so we should apply the 'max' operation to the 'lat' column in the 'station' table, and sort it in descending order. Since the unit to which the highest station latitude being calculated in the query belongs is the city, we should apply the 'group by' operation to the 'city' column in the 'station' table.

<2> Schema Linking: In this step, we identify the tables and columns that should be used based on the first step and the foreign key relationships. In this question, we only need to use table ['station'].

<3> SQL Generation: The query requires the city names in decreasing order by their highest station latitude, so we should select the 'city' column in the 'station' table. The query does not require the station latitude so it is only used for filtering and not selected. 

SQL query: SELECT city FROM station GROUP BY city ORDER BY MAX(lat) DESC


## Tables:
{}

## Foreign_keys:
{}

## Query:
{}

Let's think step by step."""

shot_prompt = """## Tables:
{}
## Foreign_keys:
{}
## Query:
{}

Let's think step by step.

{}SQL query:
{}"""

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

search_prompt = filter_search_prompt
type_prompt = filter_prompt

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
      return shot_prompt.format(x['fields'], foreign_keys, x['question'], x['reasoning'], x['predict'])
    return single_prompt.format(x['tables'], foreign_keys, x['question'])

def question_to_item(x, data):
   for xx in data:
      if xx['question'] == x:
         return xx

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-data", default='./classification/filter/filter.json', type=str)
    parser.add_argument("--train-data", default='./data/train/filter/true_samples.json', type=str)
    args = parser.parse_args()


    output_dir = os.path.join(os.path.dirname(args.test_data), 'auto_select')
    # output_dir = os.path.dirname(args.test_data)
    if not os.path.exists(output_dir):
       os.makedirs(output_dir)
    test_data = json.load(open(args.test_data, 'r'))
    train_data = json.load(open(args.train_data, 'r'))
    new_data = []
    output_file = os.path.join(output_dir, 'predict.json')
    if os.path.exists(output_file):
       new_data = json.load(open(output_file, 'r'))
       test_data = test_data[len(new_data)]

    ## fixed
    # for x in tqdm(test_data):
    #     foreign_keys = x['foreign_keys']
    #     foreign_keys = foreign_keys[foreign_keys.find('Foreign_keys = ') + len('Foreign_keys = ') : ]
    #     query = filter_prompt.format(x['fields'], foreign_keys, x['question'])
    #     response = None
    #     while response is None:
    #         try:
    #             response = GPT_generation(query)
    #         except:
    #             json.dump(new_data, open(output_file, 'w'))
    #             time.sleep(2)
    #     sql = response.rfind('SQL query: ')
    #     ans = response[sql + len('SQL query: ') :]
    #     reason = response[:sql]
    #     x.update({'reasoning' : reason, 'predict' : ans})
    #     new_data.append(x)
    # json.dump(new_data, open(output_file, 'w'))
       
    ## automation   
    matching_list = auto_prompting(test_data, train_data, shots=6)
    for i, (k, v) in tqdm(enumerate(matching_list.items())):
      test_sample = generate_single_prompt(question_to_item(k, test_data))
      train_samples = [generate_single_prompt(question_to_item(v[i], train_data)) for i in range(len(v))]
      # final_prompt = search_prompt.format(train_samples[0], train_samples[1], train_samples[2], train_samples[3], test_sample)
      final_prompt = search_prompt.format(train_samples[0], train_samples[1], train_samples[2], train_samples[3], test_sample)
      response = None
      while response is None:
        try:
            response = GPT_generation(final_prompt)
        except openai.error.InvalidRequestError:
            temp = question_to_item(k, test_data)
            foreign_keys = temp['foreign_keys']
            response = None
            foreign_keys = foreign_keys[foreign_keys.find('Foreign_keys = ') + len('Foreign_keys = ') : ]
            final_prompt = type_prompt.format(temp['tables'], foreign_keys, temp['question'])
        except:
            json.dump(new_data, open(output_file, 'w'))
      sql = response.rfind('SQL query:\n')
      ans = response[sql + len('SQL query:\n') :]
      reason = response[:sql]
      temp = test_data[i]
      temp.update({'reasoning' : reason, 'predict' : ans})
      new_data.append(temp)
    json.dump(new_data, open(output_file, 'w'))