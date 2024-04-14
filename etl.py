
import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import json

def create_conn():
    """ returns a cursor and a database connection.
    
    Returns:
        cur (psycopg2.cursor): The database cursor
        conn (psycopg2.connection): The database connection
    """
    # connect to default database
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)

    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get curser to the Database")
        print(e)

    conn.set_session(autocommit=True)
    return cur,conn

def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files
class etl:
    def __init__(self,cur,conn):
        self.cur=cur
        self.conn=conn
    def song_table(self,dir):
        songlist=get_files(dir)
        data_list=[]
        for i in range(len(songlist)):
            with open(songlist[i], 'r') as f:
                data = json.load(f)
            data_list.append(data)    
        self.df=pd.DataFrame(data_list)
        song_data=self.df[['song_id','title','artist_id','year','duration']].values[0].tolist()
        self.cur.execute(song_table_insert,song_data)
        self.conn.commit()
    def artists_table(self):
        artist_data=self.df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
        self.cur.execute(artist_table_insert,artist_data)
        self.conn.commit()         
    def time_table(self,dir):

        loglist=get_files(dir)
        data_list=[]
        for i in range(len(loglist)):
            with open(loglist[i], 'r') as f:
                for line in f:
                    data_list.append(json.loads(line))     
        df2=pd.DataFrame(data_list)
        self.df_f=df2[df2['page']=='NextSong']
        self.df_f.loc[:,'start_time']=pd.to_datetime(self.df_f['ts'], unit = 'ms')
        self.df_f.loc[:,'hour']=self.df_f['start_time'].dt.hour
        self.df_f.loc[:,'day']=self.df_f['start_time'].dt.day
        self.df_f.loc[:,'week']=self.df_f['start_time'].dt.isocalendar().week
        self.df_f.loc[:,'month']=self.df_f['start_time'].dt.month
        self.df_f.loc[:,'year']=self.df_f['start_time'].dt.year
        self.df_f.loc[:,'weekday']=self.df_f['start_time'].dt.weekday
        time_df=self.df_f[['start_time','hour','day','week','month','year','weekday']]
        time_df.values.tolist()
        for item in time_df.values.tolist():
            self.cur.execute(time_table_insert,item)
            self.conn.commit()    
    def users_table(self):
        user_df=self.df_f[['userId','firstName','lastName','gender','level']]
        user_df=user_df[user_df['userId']!='']
        for item in user_df.values.tolist():
            self.cur.execute(user_table_insert,item)
            self.conn.commit()        
    def songplays_table(self):
        fin=[]
        for index, row in self.df_f.iterrows():
            self.cur.execute(song_select,[row['song'],row['artist'],row['length']])
            res=self.cur.fetchone()
            if not res:
                ss=[]
                ss.extend([None,None,row['start_time'],row['userId'],row['level'], row['sessionId'], row['location'],row['userAgent']])
            else:
                ss=list(res)
                ss.extend([row['start_time'],row['userId'],row['level'], row['sessionId'], row['location'],row['userAgent']])
            fin.append(ss)    
        songplay=pd.DataFrame(fin,columns=['song_id','artist_id','start_time','userId','level','sessionId','location','userAgent'])   
        songplay_data=songplay[['start_time','userId','level','song_id','artist_id','sessionId','location','userAgent']]
        for item in songplay_data.values.tolist():
            self.cur.execute(songplay_table_insert,item)
            self.conn.commit()        

def main():
    cur,conn=create_conn()
    task=etl(cur,conn)
    current_dir = os.getcwd()
    file_path_song = os.path.join(current_dir, 'data\song_data')
    file_path_log = os.path.join(current_dir, 'data\log_data')
    task.song_table(file_path_song)
    task.artists_table()
    task.time_table(file_path_log)
    task.users_table()
    task.songplays_table()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()           
