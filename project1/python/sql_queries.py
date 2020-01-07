# CREATE statements in sql_queries.py 
#   specify all columns for each of the five tables with the right data types and conditions.

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# Fact Table
# songplays - records in log data associated with song plays i.e. records with page NextSong
# songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
# Review comments:
# NOT NULL constraints are proper just for the foreign keys; start_time and user_id.
# The other foreign keys song_id and artist_id can not carry this constraint because a majority of their data have NULL values and should not be eliminated.

# All the other columns do no require the NOT NULL constraint. Please remove them
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays ( \
        songplay_id SERIAL PRIMARY KEY NOT NULL, \
        start_time TIMESTAMP NOT NULL, \
        user_id INT NOT NULL, \
        level VARCHAR, \
        song_id VARCHAR, \
        artist_id VARCHAR, \
        session_id INT, \
        location VARCHAR, \
        user_agent VARCHAR \
    );
""")


# Dimension Tables
# users - users in the app
# user_id, first_name, last_name, gender, level
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users ( \
        user_id INT PRIMARY KEY UNIQUE NOT NULL, \
        first_name VARCHAR, \
        last_name VARCHAR, \
        gender VARCHAR, \
        level VARCHAR \
    );
""")

# songs - songs in music database
# song_id, title, artist_id, year, duration
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs ( \
        song_id VARCHAR PRIMARY KEY UNIQUE NOT NULL, \
        title VARCHAR, \
        artist_id VARCHAR, \
        year INT, \
        duration decimal \
    );
""")

# artists - artists in music database
# artist_id, name, location, latitude, longitude
artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists ( \
        artist_id VARCHAR PRIMARY KEY UNIQUE NOT NULL, \
        name VARCHAR, \
        location VARCHAR, \
        latitude DECIMAL, \
        longitude DECIMAL \
    );
""")

# time - timestamps of records in songplays broken down into specific units
# start_time, hour, day, week, month, year, weekday
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time ( \
        start_time TIMESTAMP NOT NULL, \
        hour INT, \
        day INT, \
        week INT, \
        month INT, \
        year INT, \
        weekday VARCHAR \
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays (
        start_time, \
        user_id, \
        level, \
        song_id, \
        artist_id, \
        session_id, \
        location, \
        user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
    INSERT INTO users (  user_id, \
                        first_name, \
                        last_name, \
                        gender, \
                        level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE \
        SET level = EXCLUDED.level || 'free';
""")

song_table_insert = ("""
    INSERT INTO songs ( song_id, \
                        title, \
                        artist_id, \
                        year, \
                        duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, \
                        name, \
                        location, \
                        latitude, \
                        longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""
    INSERT INTO time (  start_time, \
                        hour, \
                        day, \
                        week, \
                        month, \
                        year,
                        weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

# FIND SONGS

song_select = ("""
    SELECT s.song_id, a.artist_id
    FROM songs AS s
            LEFT JOIN artists AS a
                ON a.artist_id = s.artist_id
            WHERE   s.title = (%s) AND \
                    a.name = (%s)  AND \
                    s.duration = (%s);
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]