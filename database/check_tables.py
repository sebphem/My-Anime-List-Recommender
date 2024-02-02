import time
import requests
import json
import sqlite3
import os.path
from pprint import pprint

con = sqlite3.connect(os.path.dirname(__file__) + '/mal.db')
cur = con.cursor()

# print(cur.execute('SELECT MIN(ranking),MAX(ranking) FROM id_queue').fetchone())
print(cur.execute('SELECT * FROM source_lut').fetchall())
con.close()

# con = sqlite3.connect(os.path.dirname(__file__) + '/mal_nsfw_included.db')
# cur = con.cursor()
# print(cur.execute('SELECT MIN(ranking),MAX(ranking) FROM id_queue').fetchone())
# con.close()