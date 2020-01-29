# Project Intro

To build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms to a datawarehouse

# Project Goal

The analytics team to continue finding insights in what songs their users are listening to.

# Requirement
- Create an ETL pipeline that extracts data from S3
- Stage the extracted data to RedShift 
- Transform data into a set of dimensional tables
- Provide insights in what songs their users are listening to

### Concepts
1. AWS S3 Buckets [S3](https://aws.amazon.com/s3/)
2. Data modeling with [Redshift](https://aws.amazon.com/redshift/)
2. ETL pipeline using Python [Jupyter Notebook](https://jupyter.org/)

### Datasets 
Songs dataset used in the project can be found at *s3://udacity-dend/song_data*

**dataset**

Each file is in JSON format and contains metadata about a song and the artist of that song
Example record: 
```
{
  "num_songs": 1,
  "artist_id": "ARJIE2Y1187B994AB7",
  "artist_latitude": 40.7484405,
  "artist_longitude": -73.9878531,
  "artist_location": "New York",
  "artist_name": "Line Renaud",
  "song_id": "SOUPIRU12A6D4FA1E1",
  "title": "Der Kleine Dompfaff",
  "duration": 152.92036,
  "year": 2020
}
```

Log dataset used in the project can be found at *s3://udacity-dend/log_data*

**dataset**

Each file is in JSON format and contains listening event data. 

Example record: 
```
{
  "artist": "A Fine Frenzy",
  "auth": "Logged In",
  "firstName": "Anabelle",
  "gender": "F",
  "itemInSession": 0,
  "lastName": "Simpson",
  "length": 267.91138,
  "level": "free",
  "location": "Philadelphia-Camden-Wilmington, PA-NJ-DE-MD",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1541044398796,
  "sessionId": 256,
  "song": "Almost Lover (Album Version)",
  "status": 200,
  "ts": 1541377992796,
  "userAgent": "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36\"",
  "userId": "69"
}
```


### Schema 
Using the above data sets, the tables are modeled and created for queries on song play analysis. This includes the following tables.

**Fact Tables**

*songplays* - supports queries to identify song that was listened to

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables**
*users* - users in the app

user_id, first_name, last_name, gender, level

*songs* - songs in music database

song_id, title, artist_id, year, duration

*artists* - artists in music database

artist_id, name, location, lattitude, longitude

*time* - timestamps of records in songplays broken down into specific units

start_time, hour, day, week, month, year, weekday

### Structure and ETL Process
The project template includes one Jupyter Notebook file which:
1. Creates tables modeled by considering the queries that need to be supported
2. Processes the *S3* files loading them to staging tables
3. Populates the *dimension* and *fact* tables created in RedShift
4. Runs analytical queries to provide insights in what songs their users are listening to

### Analytics
![analytics](./analytics.png)



