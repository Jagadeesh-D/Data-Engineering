# Project Intro

To model user activity data to create a database and ETL pipeline for a music streaming app.

# Project Goal

The analytics team is particularly interested in understanding what songs users are listening to.

# Requirement
- Create a Postgres database with tables designed to optimize queries on song play analysis 
- Create an ETL pipeline for song play analysis 

### Concepts
1. Data modeling with [PostgreSQL](https://www.postgresql.org/)
2. Star schema for a particular analytic focus 
3. ETL pipeline using Python [Jupyter Notebook](https://jupyter.org/)

### Datasets 
The datasets used in the project can be found at */data/*

**Song dataset**

Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.
```
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```
Example record: 
```
{
   "num_songs":1,
   "artist_id":"ARJIE2Y1187B994AB7",
   "artist_latitude":null,
   "artist_longitude":null,
   "artist_location":"",
   "artist_name":"Line Renaud",
   "song_id":"SOUPIRU12A6D4FA1E1",
   "title":"Der Kleine Dompfaff",
   "duration":152.92036,
   "year":0
}
```

**Log dataset**

Each file is in JSON format and contains activity log from music streaming app based on songs in Song dataset. The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in this dataset.
```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```
Example record: 
```
{
   "artist":"Muse",
   "auth":"Logged In",
   "firstName":"Harper",
   "gender":"M",
   "itemInSession":1,
   "lastName":"Barrett",
   "length":209.50159,
   "level":"paid",
   "location":"New York-Newark-Jersey City, NY-NJ-PA",
   "method":"PUT",
   "page":"NextSong",
   "registration":1540685364796.0,
   "sessionId":275,
   "song":"Supermassive Black Hole (Twilight Soundtrack Version)",
   "status":200,
   "ts":1541721977796,
   "userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
   "userId":"42"
}
```

### Schema 
Using the song and log datasets, a star schema is created and optimized for queries on song play analysis. This includes the following tables.

**Fact Table**

*songplays* -  records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables**

*users* - users in the app
user_id, first_name, last_name, gender, level

*songs* - songs in music database
song_id, title, artist_id, year, duration

*artists* - artists in music database
artist_id, name, location, latitude, longitude

*time* - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

### Structure
*test.ipynb* displays the first few rows of each table to let you check your database.

*create_tables.py* drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.

*etl.ipynb* reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.

*etl.py* reads and processes files from song_data and log_data and loads them into your tables. You can fill this out based on your work in the ETL notebook.

*sql_queries.py* contains all your sql queries, and is imported into the last three files above.


### ETL pipeline
~~~

1. Connect to the database and get a cursor
2. Process *song_data* files one at a time looping through tree of files under */data/song_data*
	a) convert the file with JSON data to pandas object using read_json
	b) loop through each row and prepare attributes for insertion 
	c) insert artist record
	d) insert song record
3. Process *log_data* files one at a time looping through tree of files under */data/log_data*
	a) convert the file with JSON data to pandas object using read_json
	b) filter record where *page* is *NextSong*
	c) loop through each row and prepare attributes for insertion 
	c) convert ts column from ms to datetime
	d) prepare the data frame with appropriate column names
	e) insert user records
	f) identify *songid* and *artistid* based on song, artist and length
	g) prepare the record for insertion by leveraging index as primary key
	h) insert songplay records

~~~ 
