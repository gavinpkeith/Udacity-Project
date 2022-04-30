import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

#this function will process the song files, parse the data into dataframes, and insert them into the appropriate tables. This function processes the Song data and Artist data.
#This function requires a current connection to a database, and a filepath variable to the song data .json files. 
def process_song_file(cur, filepath):
    # this opens the file found at the filpath and reads it into a dataframe
    df = pd.read_json(filepath, lines=True)

    # this processes the dataframe into it's values, converts it to a list, and pulls the neccessary data out of the dataframe and inserts it into the table.
    song_data = df.values
    song_data = song_data.tolist()
    song_data_list = []
    song_data_list.append((song_data[0][7]))
    song_data_list.append((song_data[0][8]))
    song_data_list.append((song_data[0][0]))
    song_data_list.append((song_data[0][9]))
    song_data_list.append((song_data[0][5]))
    cur.execute(song_table_insert, song_data_list)
    
    # this does the same as the code above except for the artist table.
    artist_data = df.values
    artist_data = artist_data.tolist()
    artist_data_list = []
    artist_data_list.append((artist_data[0][0]))
    artist_data_list.append((artist_data[0][4]))
    artist_data_list.append((artist_data[0][2]))
    artist_data_list.append((artist_data[0][1]))
    artist_data_list.append((artist_data[0][3]))
    cur.execute(artist_table_insert, artist_data_list)


#This function will process the log files using the current connection to the database and the filpath to the log files. It creates a dataframe from the .json file, parses it into required columns and values, and inserts it into their respective tables.
def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query('page == "NextSong"')

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'])
    
    # This converts individual columns to specific datetime variables. Creates a list of column labels, and creates the final dictionary of column labels and datetime columnns. Then inserts into the appropriate table.
    time_data = t
    start_time = t
    hour = time_data.dt.hour
    day = time_data.dt.day
    week = time_data.dt.week
    month = time_data.dt.month
    year = time_data.dt.year
    weekday = time_data.dt.weekday
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = {"start_time": start_time, "hour": hour, "day": day, "week": week, "month": month, "year": year, "weekday": weekday}
    time_df = pd.DataFrame(time_df)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # loads user table from the dataframe
    user_df = df.copy()
    user_df.drop(['artist', 'auth', 'itemInSession', 'length', 'location', 'method', 'page', 'registration', 'sessionId', 'song', 'status', 'ts', 'userAgent'], axis=1, inplace=True)
    user_df = user_df[['userId', 'firstName', 'lastName', 'gender', 'level']]

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
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent) 
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
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
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()