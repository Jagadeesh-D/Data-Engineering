# Project Intro

To model user activity data to create a database and ETL pipeline for a music streaming app.

# Project Goal

The analytics team is particularly interested in understanding what songs users are listening to.

# Requirement
- Create a Apache Cassandra database with tables designed to optimize queries on song play analysis 
- Create an ETL pipeline for song play analysis 

### Concepts
1. Data modeling with [Apache Cassandra](http://cassandra.apache.org/)
2. ETL pipeline using Python [Jupyter Notebook](https://jupyter.org/)

### Datasets 
The datasets used in the project can be found at */event_data/*

**dataset**

Each file is in CSV format and contains listening event data. The files are partitioned by the date. For example, here are filepaths to two files in this dataset.
```
event_data/2018-11-01-events.csv
event_data/2018-11-02-events.csv
```
Example record: 
```
"A Fine Frenzy","Anabelle","F","0","Simpson","267.91138","free","Philadelphia-Camden-Wilmington, PA-NJ-DE-MD","256","Almost Lover (Album Version)","69"
```

### Schema 
Using the event data set, the tables are modeled and created for queries on song play analysis. This includes the following tables.

**Tables**

*sessions* - supports queries to identify song that was listened in a specific session/item combination
session_id, item_in_session, artist_name, song, length

*user_sessions* - supports queries to identify what songs user listened to in a session(listing them in the order listened)
user_id, session_id, artist_name, song, first_name, last_name, item_in_session

*song_listeners* - supports queries to identify what users listened to a particular song
song, user_id, first_name, last_name

### Structure
The project template includes one Jupyter Notebook file which:
1. Processes the *event_datafile_new.csv* dataset to create a denormalized dataset
2. Load the data into tables you create in Apache Cassandra
3. Models the data tables considering the queries that need to be supported
4. Running the queries used to model your data tables for to test the data


