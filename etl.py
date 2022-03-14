import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This procedure processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """
    # open song file
    df = pd.read_json(filepath, typ='series')
    
    # insert artist record
    artist_data = list(df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values)
    cur.execute(artist_table_insert, artist_data)

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values)
    cur.execute(song_table_insert, song_data)
    


def process_log_file(cur, filepath):
    """
    This procedure processes a log file whose filepath has been provided as an arugment.
    It filters the logs in order to process log only when page = NextSong.
    It extracts the timestamp information and calculates required values and stores it into the time table.
    Then it extracts the user information and stores it into the users table.
    Finally, For every log, it gets respective song ID and artist ID from database using song_select query
    And stores all the required information in songplays table.
    
    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the log file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query("page == 'NextSong'")

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit = 'ms')
    
    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    '''
    # For row by row insertion
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
    '''

    # Multi insert at once
    cur.executemany(time_table_insert, [tuple(x) for x in time_df.to_numpy()])

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    '''
    # For row by row insertion
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    '''

    # Multi insert at once
    cur.executemany(user_table_insert, [tuple(x) for x in user_df.to_numpy()])

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
        songplay_data = (pd.to_datetime(row.ts), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This procedure crawls over the file directory passed as filepath argument
    And populates a list of full paths of json files in it.
    It then iterates over this list of json files 
    And pass each file to the function passed as func argument along with the cursor variable cur.
    This procedure is also responsible for commiting actions to database after every execution of func.
    
    INPUTS:
    * cur the cursor variable
    * conn the connection variable
    * filepath the file path to the base folder
    * func the function to be called
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
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
        The main function is establishes connection and cursor to the database.
        Executes process_data method for both song_data and log_data folders.
        Closes the connection to the database in the end.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()