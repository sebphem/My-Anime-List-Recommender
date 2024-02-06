import time
import requests
import json
import sqlite3
import os.path
from pprint import pprint

con = sqlite3.connect(os.path.dirname(__file__) + '/mal.db')
cur = con.cursor()

def check_something_in_the_tables():
    print(cur.execute('SELECT DISTINCT status FROM id_queue').fetchall())
    print(cur.execute('SELECT count(status) FROM id_queue WHERE status ="done"').fetchall())
    print(cur.execute('SELECT count(status) FROM id_queue WHERE status = "waiting"').fetchall())
    print(cur.execute('SELECT COUNT(*) FROM anime_info').fetchall())
    con.commit()
    # con.close()

def reset_iq_queue():
    cur.execute('UPDATE id_queue SET status = "waiting" WHERE 1=1')
    con.commit()
    # con.close()

def add_row_to_tables():
    cur.execute('ALTER TABLE id_queue DROP status')
    cur.execute('ALTER TABLE id_queue ADD status string DEFAULT "waiting"')
    con.commit()
    # con.close()

def make_id_queue_backup():
    cur.execute('''
                    CREATE TABLE IF NOT EXISTS id_queue_backup AS
                    SELECT * FROM id_queue;''')
    con.commit()

def check_nsfw_diffs():
    con = sqlite3.connect(os.path.dirname(__file__) + '/mal_nsfw_included.db')
    cur = con.cursor()
    print(cur.execute('SELECT MIN(ranking),MAX(ranking) FROM id_queue').fetchone())
    # con.close()

reset_iq_queue()
check_something_in_the_tables()