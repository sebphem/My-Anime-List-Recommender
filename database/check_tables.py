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
    print('all id_queue rows: ',cur.execute('SELECT count(status) FROM id_queue').fetchone())
    print(cur.execute('SELECT count(status) FROM id_queue WHERE status ="done"').fetchone())
    print(cur.execute('SELECT count(status) FROM id_queue WHERE status = "waiting"').fetchone())
    print(cur.execute('SELECT ROWID FROM id_queue WHERE title ="Wo Shi Da Xiongmao"').fetchone())
    print(cur.execute('SELECT ROWID FROM id_queue WHERE title ="Wo Shi Faming Jia"').fetchone())
    print(cur.execute('SELECT ROWID FROM id_queue WHERE title ="Wo Shi Lang: Huolong Shanda Maoxian"').fetchone())
    print(cur.execute('SELECT * FROM id_queue ORDER BY ROWID LIMIT 5').fetchall())
    con.commit()
    # con.close()

def reupdate_id_queue_rows():
    cur.execute('''UPDATE id_queue
                SET status = 'done'
                WHERE ROWID <= 14091
                ''')
    con.commit()

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

# reset_iq_queue()
reupdate_id_queue_rows()
check_something_in_the_tables()