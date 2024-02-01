from configparser import ConfigParser
from pprint import pprint
from functools import wraps
import os.path
import time
import requests
import json
import sqlite3
con = sqlite3.connect(os.path.dirname(__file__) + '/mal.db')
cur = con.cursor()

#############################
# https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
###############################

with open('keys/mal_token.json') as f:
    keys = json.load(f)

base_url = "https://api.myanimelist.net/v2"

def test_one_piece():
    res = requests.get(base_url+'/anime', params={'q':'one','limit':4},
                    headers={'Authorization': f'Bearer {keys["access_token"]}'})
    print(res.url)
    return res.json()

def test_anime_ranking():
    res = requests.get(base_url+'/anime/ranking', params={'ranking_type':'all','limit':500,'offset':500},
                    headers={'Authorization': f'Bearer {keys["access_token"]}'})
    print(res.url)
    return res.json()

@timeit
def mine_40000_anime():
    #just good mining
    for i in range(0,40000,500):
        print(12*'-')
        print("getting anime ", i,"-",i+499,"/40000")
        if i == 0:
            res = requests.get(base_url+'/anime/ranking', params={'ranking_type':'all','limit':500},
                            headers={'Authorization': f'Bearer {keys["access_token"]}'})
        else:
            res = requests.get(base_url+'/anime/ranking', params={'ranking_type':'all','limit':500,'offset':i},
                                headers={'Authorization': f'Bearer {keys["access_token"]}'})
        print(res.url)
        anime_info_json = res.json()['data']
        anime_info_list =[]
        for one_anime_data in anime_info_json:
            anime_info_list.append([one_anime_data['node']['id'],one_anime_data['node']['title'],one_anime_data['ranking']['rank']])
        cur.executemany('INSERT INTO id_queue (id, title, ranking) VALUES(?, ?, ?)',anime_info_list)
        con.commit()
        break
# pprint(test_anime_ranking())
mine_40000_anime()