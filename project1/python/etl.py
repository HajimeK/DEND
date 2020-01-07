# The script, etl.py, runs in the terminal without errors. The script connects to the Sparkify database, #extracts and processes the log_data and song_data, and loads data into the five tables.
#
# Since this is a subset of the much larger dataset,
# the solution dataset will only have 1 row match that will populate a songid
# and an artistid in the fact table. Those are the only 2 values
# that the query in the sql_queries.py will return.
# The rest will be none values.
#
# INSERT statements are correctly written for each tables
# and handles existing records where appropriate.
# songs and artists tables are used to retrieve the correct information for the songplays INSERT.

import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process song files and store them into songs and artists table in DB.
    The files includes JSON format of songs data.

    Parameters
    ----------
    cur : Cursor class instance (http://initd.org/psycopg/docs/cursor.html)
        database cursor
    filepath : string
        full file path to entry data

    Returns
    -------
    song_data in songs table as a row
    artist_data in artists table as a row
    """
    # open song file
    df = pd.read_json(filepath, lines=True, orient='columns')

    # insert song record
    song_data = (df.values[0][6], df.values[0][7], df.values[0][1], df.values[0][9], df.values[0][8])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = (df.values[0][1], df.values[0][5], df.values[0][4], df.values[0][2], df.values[0][3])
    #print(artist_data)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process log_data files and store them into songplays, users, and timetable in DB.
    The files includes JSON format data.

    Parameters
    ----------
    cur : Cursor class instance (http://initd.org/psycopg/docs/cursor.html)
        database cursor
    filepath : string
        full file path to entry data

    Returns
    -------
    Add rows in the table songplays
    Add rows in the table users
    Add rows in the table time
    """
    # open log file
    df = pd.read_json(filepath, lines=True, orient='columns')

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = list(zip(t.dt.strftime('%Y-%m-%d %I:%M:%S'), t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:,['userId','firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        start_time = pd.to_datetime(row.ts, unit='ms').strftime('%Y-%m-%d %I:%M:%S')
        songplay_data = (start_time, row.userId, row.level, str(songid), str(artistid), row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Navigate through song_data / log_data files and call processing functions accordingly
    to store data in the PostgreSQL database connected by the caller function.

    Parameters
    ----------
    cur : Cursor class instance (http://initd.org/psycopg/docs/cursor.html)
        database cursor
    conn : Connection class instance
        databqase connection.
    filepath : string
        full file path to entry data
    func : Python function
        Function to process files and their contents.

    Returns
    -------
    The progress is logged in the console.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Connect to DB to store all the input data from data/song_data and data/log_data.
    """
    conn = psycopg2.connect(
        "host=172.17.0.2 dbname=sparkifydb user=student password=student")
#        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
