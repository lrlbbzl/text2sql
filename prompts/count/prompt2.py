count_reasoning_generate_prompt = """You are a powerful text-to-SQL reasoner. I now want to convert complex text queries into analytical statements that facilitate SQL statement generation. Please learn from the examples given, analysis the query step by step, and find the tables needed for each problem.


Example 1:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table gymnast, columns = [*,Gymnast_ID,Floor_Exercise_Points,Pommel_Horse_Points,Rings_Points,Vault_Points,Parallel_Bars_Points,Horizontal_Bar_Points,Total_Points]
Table people, columns = [*,People_ID,Name,Age,Height,Hometown]

"foreign_keys":
[gymnast.Gymnast_ID = people.People_ID]

user query:
How many gymnasts are from each hometown?

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the number of gymnasts from each hometown, so we should apply the 'count' operation to table 'gymnast', and it does not need sort. Since the unit to which the gymnasts being counted in the query belong is hometown and only table 'people' has column 'Hometown', so we should apply the 'group by' operation to column 'Hometown' in table 'people'. 

Secondly, we need to retrieve the hometown, so we should join table 'people'. The query requires the count of gymnasts, so it needs to be selected.

Finally, based on the above analysis and requirements in user query, we need to use tables ['gymnast', 'people'].


Example 2:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table county, columns = [*,County_Id,County_name,Population,Zip_code]
Table election, columns = [*,Election_ID,Counties_Represented,District,Delegate,Party,First_Elected,Committee]
Table party, columns = [*,Party_ID,Year,Party,Governor,Lieutenant_Governor,Comptroller,Attorney_General,US_Senate]

"foreign_keys":
[election.District = county.County_Id,election.Party = party.Party_ID]

user query:
Show the name of each party and the corresponding number of delegates from that party.

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the number of delegates of each party, so we should apply the 'count' operation to table 'election'. Since the unit to which the delegates being counted in the query belong is party, table 'party' and 'election' both have column 'Party'. But the main focus of this query is on party, so we should apply the 'group by' operation to column 'Party' in table 'party'. 

Secondly, we need to retrieve the name of party. The query requires the count of delegates, so it needs to be selected. Please pay attention to the selecting order.

Finally, based on the above analysis and requirements in user query, we need to use tables ['party', 'election'].


Example 3:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table city, columns = [*,City_ID,Official_Name,Status,Area_km_2,Population,Census_Ranking]
Table competition_record, columns = [*,Competition_ID,Farm_ID,Rank]
Table farm, columns = [*,Farm_ID,Year,Total_Horses,Working_Horses,Total_Cattle,Oxen,Bulls,Cows,Pigs,Sheep_and_Goats]
Table farm_competition, columns = [*,Competition_ID,Year,Theme,Host_city_ID,Hosts]

"foreign_keys":
[farm_competition.Host_city_ID = city.City_ID,competition_record.Farm_ID = farm.Farm_ID,competition_record.Competition_ID = farm_competition.Competition_ID]

user query:
Show the status of the city that has hosted the greatest number of competitions.

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the city that has hosted greatest number of competitions, so we should apply the 'count' operation to column 'Competition_ID' in table 'farm_competition', and sort it in descending order. Since the unit to which the competitions being counted in the query belong is city and only table 'farm_competition' has column 'Host_city_ID', so we should apply the 'group by' operation to column 'Host_city_ID' in table 'farm_competition'.

Secondly, we need to retrieve the status of cities selected in the first step, so we should join table 'city '. The query does not require the count of most competitions, so it is only used for filtering and not selected. 

Finally, based on the above analysis and requirements in user query, we need to use tables ['farm_competion', 'city'].


Example 4:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
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

"foreign_keys":
[albums.artist_id = artists.id,employees.reports_to = employees.id,customers.support_rep_id = employees.id,invoices.customer_id = customers.id,tracks.media_type_id = media_types.id,tracks.genre_id = genres.id,tracks.album_id = albums.id,invoice_lines.track_id = tracks.id,invoice_lines.invoice_id = invoices.id,playlist_tracks.track_id = tracks.id,playlist_tracks.playlist_id = playlists.id]

user query:
A list of the top 10 countries by average invoice size. List country name and average invoice size.

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the countries ordered by average invoice size, so we should apply the 'avg' operation to column 'total' in table 'invoices', and sort it in descending order. Since the unit to which the invoices being counted in the query belong is country and only table 'invoices' has column 'billing_country', so we should apply the 'group by' operation to column 'billing_country' in table 'invoices'.

Secondly, we need to retrieve the country name and average invoice size. Please pay attention to the selecting order.

Finally, based on the above analysis and requirements in user query, we only need to use table ['invoices'].


Example 5:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table game, columns = [*,stadium_id,id,Season,Date,Home_team,Away_team,Score,Competition]
Table injury_accident, columns = [*,game_id,id,Player,Injury,Number_of_matches,Source]
Table stadium, columns = [*,id,name,Home_Games,Average_Attendance,Total_Attendance,Capacity_Percentage]

"foreign_keys":
[game.stadium_id = stadium.id,injury_accident.game_id = game.id]

user query:
What are the ids, scores, and dates of the games which caused at least two injury accidents?

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the games which caused at least two injury accidents, so we should apply the 'count' operation to table 'injury_accident', and set the condition 'count >= 2'. Since the unit to which the injury accidents being counted in the query belong is game and only table 'injury_accident' has column 'game_id', so we should apply the 'group by' operation to column 'game_id' in table 'injury_accident'.

Secondly, we need to retrieve the ids, scores and dates of the games selected in the first step, so we should join table game. Please pay attention to the selecting order.

Finally, based on the above analysis and requirements in user query, we need to use tables ['game', 'injury_accident'].


Example 6:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table Addresses, columns = [*,address_id,address_content,city,zip_postcode,state_province_county,country,other_address_details]
Table Customer_Addresses, columns = [*,customer_id,address_id,date_address_from,address_type,date_address_to]
Table Customer_Contact_Channels, columns = [*,customer_id,channel_code,active_from_date,active_to_date,contact_number]
Table Customer_Orders, columns = [*,order_id,customer_id,order_status,order_date,order_details]
Table Customers, columns = [*,customer_id,payment_method,customer_name,date_became_customer,other_customer_details]
Table Order_Items, columns = [*,order_id,product_id,order_quantity]
Table Products, columns = [*,product_id,product_details]

"foreign_keys":
[Customer_Addresses.customer_id = Customers.customer_id,Customer_Addresses.address_id = Addresses.address_id,Customer_Contact_Channels.customer_id = Customers.customer_id,Customer_Orders.customer_id = Customers.customer_id,Order_Items.order_id = Customer_Orders.order_id,Order_Items.product_id = Products.product_id]

user query:
What are the names of customers using the most popular payment method?

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the most popular payment method, and the popularity is related to the number of people using it. So we should apply the 'count' operation to table 'Customers'. Since the unit to which the people being counted in the query belong is payment_method and only table 'Customers' has column 'payment_method', so we should apply the 'group by' operation to column 'payment_method' in table 'Customers'.

Secondly, we need to retrieve the names of customers, filtered by payment method selected in the first step. The query does not require the count of most popular payemnt method, so it is only used for filtering and not selected.

Finally, based on the above analysis and requirements in user query, we only need to use table ['Customers'].


"""


count_sql_generate_prompt = """You are a powerful text-to-SQL reasoner. I now want to convert complex text queries into analytical statements that facilitate SQL statement generation. Please learn from the examples given, determine whether the problem needs to be decomposed, and find the tables needed for each problem after decomposed.


Example 1:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table gymnast, columns = [*,Gymnast_ID,Floor_Exercise_Points,Pommel_Horse_Points,Rings_Points,Vault_Points,Parallel_Bars_Points,Horizontal_Bar_Points,Total_Points]
Table people, columns = [*,People_ID,Name,Age,Height,Hometown]

"foreign_keys":
[gymnast.Gymnast_ID = people.People_ID]

user query:
How many gymnasts are from each hometown?

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the number of gymnasts from each hometown, so we should apply the 'count' operation to table 'gymnast', and it does not need sort. Since the unit to which the gymnasts being counted in the query belong is hometown and only table 'people' has column 'Hometown', so we should apply the 'group by' operation to column 'Hometown' in table 'people'. 

Secondly, we need to retrieve the hometown, so we should join table 'people'. The query requires the count of gymnasts, so it needs to be selected.

Finally, based on the above analysis and requirements in user query, we need to use tables ['gymnast', 'people'].

SQL query: SELECT T2.Hometown ,  COUNT(*) FROM gymnast AS T1 JOIN people AS T2 ON T1.Gymnast_ID  =  T2.People_ID GROUP BY T2.Hometown


Example 2:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table county, columns = [*,County_Id,County_name,Population,Zip_code]
Table election, columns = [*,Election_ID,Counties_Represented,District,Delegate,Party,First_Elected,Committee]
Table party, columns = [*,Party_ID,Year,Party,Governor,Lieutenant_Governor,Comptroller,Attorney_General,US_Senate]

"foreign_keys":
[election.District = county.County_Id,election.Party = party.Party_ID]

user query:
Show the name of each party and the corresponding number of delegates from that party.

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the number of delegates of each party, so we should apply the 'count' operation to table 'election'. Since the unit to which the delegates being counted in the query belong is party, table 'party' and 'election' both have column 'Party'. But the main focus of this query is on party, so we should apply the 'group by' operation to column 'Party' in table 'party'. 

Secondly, we need to retrieve the name of party. The query requires the count of delegates, so it needs to be selected. Please pay attention to the selecting order.

Finally, based on the above analysis and requirements in user query, we need to use tables ['party', 'election'].

SQL query: SELECT T1.Party , COUNT(*) FROM party AS T1 JOIN election AS T2 ON T1.Party_ID = T2.Party GROUP BY T1.Party


Example 3:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table city, columns = [*,City_ID,Official_Name,Status,Area_km_2,Population,Census_Ranking]
Table competition_record, columns = [*,Competition_ID,Farm_ID,Rank]
Table farm, columns = [*,Farm_ID,Year,Total_Horses,Working_Horses,Total_Cattle,Oxen,Bulls,Cows,Pigs,Sheep_and_Goats]
Table farm_competition, columns = [*,Competition_ID,Year,Theme,Host_city_ID,Hosts]

"foreign_keys":
[farm_competition.Host_city_ID = city.City_ID,competition_record.Farm_ID = farm.Farm_ID,competition_record.Competition_ID = farm_competition.Competition_ID]

user query:
Show the status of the city that has hosted the greatest number of competitions.

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the city that has hosted greatest number of competitions, so we should apply the 'count' operation to column 'Competition_ID' in table 'farm_competition', and sort it in descending order. Since the unit to which the competitions being counted in the query belong is city and only table 'farm_competition' has column 'Host_city_ID', so we should apply the 'group by' operation to column 'Host_city_ID' in table 'farm_competition'.

Secondly, we need to retrieve the status of cities selected in the first step, so we should join table 'city '. The query does not require the count of most competitions, so it is only used for filtering and not selected. 

Finally, based on the above analysis and requirements in user query, we need to use tables ['farm_competion', 'city'].

SQL query: SELECT T1.Status FROM city AS T1 JOIN farm_competition AS T2 ON T1.City_ID  =  T2.Host_city_ID GROUP BY T2.Host_city_ID ORDER BY COUNT(*) DESC LIMIT 1


Example 4:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
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

"foreign_keys":
[albums.artist_id = artists.id,employees.reports_to = employees.id,customers.support_rep_id = employees.id,invoices.customer_id = customers.id,tracks.media_type_id = media_types.id,tracks.genre_id = genres.id,tracks.album_id = albums.id,invoice_lines.track_id = tracks.id,invoice_lines.invoice_id = invoices.id,playlist_tracks.track_id = tracks.id,playlist_tracks.playlist_id = playlists.id]

user query:
A list of the top 10 countries by average invoice size. List country name and average invoice size.

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the countries ordered by average invoice size, so we should apply the 'avg' operation to column 'total' in table 'invoices', and sort it in descending order. Since the unit to which the invoices being counted in the query belong is country and only table 'invoices' has column 'billing_country', so we should apply the 'group by' operation to column 'billing_country' in table 'invoices'.

Secondly, we need to retrieve the country name and average invoice size. Please pay attention to the selecting order.

Finally, based on the above analysis and requirements in user query, we only need to use table ['invoices'].

SQL query: SELECT billing_country ,  AVG(total) FROM invoices GROUP BY billing_country ORDER BY AVG(total) DESC LIMIT 10;


Example 5:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table game, columns = [*,stadium_id,id,Season,Date,Home_team,Away_team,Score,Competition]
Table injury_accident, columns = [*,game_id,id,Player,Injury,Number_of_matches,Source]
Table stadium, columns = [*,id,name,Home_Games,Average_Attendance,Total_Attendance,Capacity_Percentage]

"foreign_keys":
[game.stadium_id = stadium.id,injury_accident.game_id = game.id]

user query:
What are the ids, scores, and dates of the games which caused at least two injury accidents?

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the games which caused at least two injury accidents, so we should apply the 'count' operation to table 'injury_accident', and set the condition 'count >= 2'. Since the unit to which the injury accidents being counted in the query belong is game and only table 'injury_accident' has column 'game_id', so we should apply the 'group by' operation to column 'game_id' in table 'injury_accident'.

Secondly, we need to retrieve the ids, scores and dates of the games selected in the first step, so we should join table game. Please pay attention to the selecting order.

Finally, based on the above analysis and requirements in user query, we need to use tables ['game', 'injury_accident'].

SQL query: SELECT T1.id ,  T1.score ,  T1.date FROM game AS T1 JOIN injury_accident AS T2 ON T2.game_id  =  T1.id GROUP BY T1.id HAVING count(*)  >=  2


Example 6:
The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
Table Addresses, columns = [*,address_id,address_content,city,zip_postcode,state_province_county,country,other_address_details]
Table Customer_Addresses, columns = [*,customer_id,address_id,date_address_from,address_type,date_address_to]
Table Customer_Contact_Channels, columns = [*,customer_id,channel_code,active_from_date,active_to_date,contact_number]
Table Customer_Orders, columns = [*,order_id,customer_id,order_status,order_date,order_details]
Table Customers, columns = [*,customer_id,payment_method,customer_name,date_became_customer,other_customer_details]
Table Order_Items, columns = [*,order_id,product_id,order_quantity]
Table Products, columns = [*,product_id,product_details]

"foreign_keys":
[Customer_Addresses.customer_id = Customers.customer_id,Customer_Addresses.address_id = Addresses.address_id,Customer_Contact_Channels.customer_id = Customers.customer_id,Customer_Orders.customer_id = Customers.customer_id,Order_Items.order_id = Customer_Orders.order_id,Order_Items.product_id = Products.product_id]

user query:
What are the names of customers using the most popular payment method?

Decompose and find the tables to be used:

Let's think step by step.

Firstly, the query requires the most popular payment method, and the popularity is related to the number of people using it. So we should apply the 'count' operation to table 'Customers'. Since the unit to which the people being counted in the query belong is payment_method and only table 'Customers' has column 'payment_method', so we should apply the 'group by' operation to column 'payment_method' in table 'Customers'.

Secondly, we need to retrieve the names of customers, filtered by payment method selected in the first step. The query does not require the count of most popular payemnt method, so it is only used for filtering and not selected.

Finally, based on the above analysis and requirements in user query, we only need to use table ['Customers'].

SQL query: SELECT customer_name FROM customers WHERE payment_method  =  (SELECT payment_method FROM customers GROUP BY payment_method ORDER BY count(*) DESC LIMIT 1)


The following is a description of a SQL database, including the tables it contains and the foreign key correspondences in each table. A user query is given afterward.

"tables":
{}

"foreign_keys":
{}

user query:
{}

Decompose and find the tables to be used:

Let's think step by step.

{}

SQL query: 
"""
