import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

# DROP STAGING TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"

# DROP FACT TABLES (Always prior to dimensions)
songplay_table_drop = "DROP TABLE IF EXISTS songplays"

# DROP DIMENSION TABLES
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
user_table_drop = "DROP TABLE IF EXISTS users"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# STAGING TABLES
staging_events_table_create= ("""CREATE TABLE staging_events(
    event_id INT IDENTITY(0,1),
    artist_name VARCHAR(500),
    auth VARCHAR(50),
    first_name VARCHAR(100),
    gender  VARCHAR(1),
    item_in_session SMALLINT,
    last_name VARCHAR(100),
    length DECIMAL(10,6), 
    level VARCHAR(25),
    location VARCHAR(100),
    method VARCHAR(25),
    page VARCHAR(25),
    registration VARCHAR(50),
    session_id BIGINT,
    song VARCHAR(255),
    status SMALLINT,
    ts VARCHAR(50),
    user_agent TEXT,
    user_id VARCHAR(10) NOT NULL,
    PRIMARY KEY (event_id))
""")

staging_songs_table_create = ("""CREATE TABLE staging_songs(
    song_id VARCHAR(50) NOT NULL,
    num_songs SMALLINT,
    artist_id VARCHAR(50) NOT NULL,
    artist_latitude DECIMAL(10,7),
    artist_longitude DECIMAL(10,7),
    artist_location VARCHAR(250),
    artist_name VARCHAR(500),
    title VARCHAR(255) NOT NULL,
    duration DECIMAL(10,6) NOT NULL,
    year INT NOT NULL,
    PRIMARY KEY (song_id))
""")

# DIMENSION TABLES
# timestamps of records in songplays broken down into specific units
time_table_create = ("""CREATE TABLE time(
    start_time TIMESTAMP,
    hour SMALLINT,
    day SMALLINT,
    week SMALLINT,
    month SMALLINT,
    year INT,
    weekday SMALLINT,
    PRIMARY KEY (start_time))
""")

# users
user_table_create = ("""CREATE TABLE users(
    user_id INT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(1),
    level VARCHAR(25),
    PRIMARY KEY (user_id))
""")

# artists
artist_table_create = ("""CREATE TABLE artists(
    artist_id VARCHAR(50),
    name VARCHAR(255),
    location VARCHAR(255),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    PRIMARY KEY (artist_id))
""")

# songs
song_table_create = ("""CREATE TABLE songs(
    song_id VARCHAR(50),
    title VARCHAR(255) NOT NULL,
    artist_id VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    duration DECIMAL(10,6) NOT NULL,
    PRIMARY KEY (song_id))
""")

# FACT TABLE
# records in event data associated with song plays i.e. records with page NextSong
songplay_table_create = ("""CREATE TABLE songplays(
    songplay_id INT IDENTITY(0,1),
    start_time TIMESTAMP REFERENCES time(start_time),
    user_id VARCHAR(50) REFERENCES users(user_id),
    level VARCHAR(25),
    song_id VARCHAR(50) REFERENCES songs(song_id),
    artist_id VARCHAR(50) REFERENCES artists(artist_id),
    session_id BIGINT,
    location VARCHAR(100),
    user_agent TEXT,
    PRIMARY KEY (songplay_id))
""")


# LOAD STAGING TABLES

staging_events_copy = ("""copy staging_events 
    from '{}'
    credentials 'aws_iam_role={}'
    region 'us-west-2' 
    FORMAT AS JSON '{}'
    """).format(config.get('S3','LOG_DATA'), 
                config.get('IAM_ROLE', 'ARN'),
                config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""copy staging_songs 
    from '{}'
    credentials 'aws_iam_role={}'
    region 'us-west-2' 
    JSON 'auto'
    """).format(config.get('S3','SONG_DATA'), 
            config.get('IAM_ROLE', 'ARN'))

# LOAD DIMENSION TABLES
time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT 
    start_time, 
    EXTRACT(h from start_time) AS hour,
    EXTRACT(d from start_time) AS day,
    EXTRACT(w from start_time) AS week,
    EXTRACT(mon from start_time) AS month,
    EXTRACT(y from start_time) AS year, 
    EXTRACT(weekday from start_time) AS weekday 
    FROM 
    (
        SELECT DISTINCT  timestamp 'epoch' + ts/1000 * interval '1 second' as start_time
        FROM staging_events s     
    )
""")

# ASSUMPTION: Data may have same user with different levels. In these cases we pick max i.e, consider them as paid for demo purposes
user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender)
    SELECT DISTINCT 
        cast(user_id as int),
        first_name,
        last_name,
        gender
    FROM staging_events
    WHERE len(user_id) > 0
""")

user_table_update = ("""UPDATE users 
    SET level = MaxLevel
    FROM 
    (
        SELECT DISTINCT cast(user_id as int) user_id, max(level) MaxLevel 
        FROM staging_events 
        WHERE len(user_id) > 0 
        GROUP BY cast(user_id as int)
    ) Temp
    JOIN users U on U.user_id = Temp.user_id
""")

# ASSUMPTION: Data may have same artist ID with different names. In these cases we pick max for demo purposes
artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT 
        artist_id,
        max(artist_name) as artist_name
    FROM staging_songs
    WHERE len(artist_id) > 0 and len(artist_name)>0
    GROUP BY artist_id
""")

artist_table_update = ("""UPDATE artists 
    SET location = artist_location, latitude=artist_latitude, longitude=artist_longitude
    FROM 
    (
        SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude 
        FROM staging_songs 
        WHERE len(artist_location) > 0 and len(artist_latitude)>0 and len(artist_longitude) > 0
    ) Temp
    JOIN artists A on A.artist_id = Temp.artist_id
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT 
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE year > 0
""")

# LOAD FACT TABLES
songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT 
        TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time, 
        se.user_id, 
        se.level,
        ss.song_id,
        ss.artist_id,
        se.session_id,
        se.location,
        se.user_agent
    FROM staging_events se, staging_songs ss
    WHERE se.song = ss.title
    AND se.artist_name = ss.artist_name
    AND se.page = 'NextSong'
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, user_table_update, song_table_insert, artist_table_insert, artist_table_update, time_table_insert]