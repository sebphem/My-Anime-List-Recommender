import sqlite3
import os.path
con = sqlite3.connect(os.path.dirname(__file__) +'/mal.db')
cur = con.cursor()

def make_info_queue():
    # Because anime ranking only holds basic data, make a queue to find out more information
    # https://myanimelist.net/apiconfig/references/api/v2#operation/anime_ranking_get
    cur.executescript('''
                DROP TABLE IF EXISTS id_queue;
                CREATE TABLE id_queue(
                    id int UNIQUE,
                    title string UNIQUE,
                    ranking int,
                    PRIMARY KEY (id)
                )
                ''')
    con.commit()

def make_anime_info_table():
    #store most of the information
    #https://myanimelist.net/apiconfig/references/api/v2#operation/anime_anime_id_get
    pass

make_info_queue()