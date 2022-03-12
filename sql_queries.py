# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INT NOT NULL IDENTITY PRIMARY KEY,
        start_time VARCHAR REFERENCES time (start_time),
        user_id INT REFERENCES users(user_id),
        level VARCHAR REFERENCES users(level),
        song_id INT REFERENCES songs(song_id),
        artist_id INT REFERENCES artists(artist_id),
        session_id INT,
        location VARCHAR,
        user_agent VARCHAR
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INT NOT NULL IDENTITY PRIMARY KEY,
        first_name VARCHAR,
        last_name VARCHAR,
        gender CHAR(1),
        level VARCHAR
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs(
        song_id INT NOT NULL IDENTITY PRIMARY KEY,
        title VARCHAR,
        artist_id INT REFERENCES artists(artist_id),
        year INT,
        duration FLOAT
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists(
        artist_id INT NOT NULL IDENTITY PRIMARY KEY,
        name VARCHAR,
        location VARCHAR,
        latitude FLOAT,
        longitude FLOAT
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time(
        start_time LONG NOT NULL PRIMARY KEY,
        hour INT,
        day INT,
        WEEK INT,
        month INT,
        year INT,
        weekday INT    
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
""")

user_table_insert = ("""
    INSERT INTO users (first_name, last_name, gender, level) VALUES (%s,%s,%s,%s)
""")

song_table_insert = ("""
    INSERT INTO songs (title, artist_id, year, duration) VALUES (%s, %s, %s, %s)
""")

artist_table_insert = ("""
    INSERT INTO artists (name, location, latitude, longitude) VALUES (%s,%s,%s,%s)
""")


time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]