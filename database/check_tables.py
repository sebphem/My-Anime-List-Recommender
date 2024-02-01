import time
import requests
import json
import sqlite3
import os.path
from pprint import pprint

con = sqlite3.connect(os.path.dirname(__file__) + '/mal.db')
cur = con.cursor()

print(cur.execute('SELECT * FROM id_queue').fetchall())