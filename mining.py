from configparser import ConfigParser
from pprint import pprint
from functools import wraps
from matplotlib import pyplot as plt
import os.path
import time
import requests
import json
import sqlite3
con = sqlite3.connect(os.path.dirname(__file__) + '/database/mal.db')
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
def get_in_depth_info_for_each_anime():
    #just good mining
    relation_lut = ['sequel', 'prequel', 'alternative_setting', 'alternative_version', 'side_story', 'parent_story', 'summary', 'full_story']
    source_lut = ['other', 'original', 'manga', '4_koma_manga', 'web_manga', 'digital_manga', 'novel', 'light_novel', 'visual_novel', 'game', 'card_game', 'book', 'picture_book', 'radio', 'music']
    rating_lut = ['g', 'pg', 'pg_13', 'r', 'r+', 'Hentai']
    status_lut = ['finished_airing', 'currently_airing', 'not_yet_aired']
    media_lut = ['unknown', 'tv', 'ova', 'movie', 'special', 'ona', 'music']
    season_lut = ['winter', 'spring','summer','fall']
    genres_lut = ['','Action','Adventure']
    latencies = []
    num_of_anime = cur.execute('SELECT COUNT(*) FROM id_queue').fetchone()[0]
    print("num of anime: ", num_of_anime)
    for i in range(0, num_of_anime, 1):
        ###########
        # Console #
        ###########
        print(12*'-')
        print("getting anime ", i,"/",num_of_anime)
        ###########
        # Request #
        ###########
        start_time = time.time()
        res = requests.get(f'{base_url}/anime/{i}', params={'fields':'id,title,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,num_episodes,start_season,broadcast,source,average_episode_duration,rating,related_anime,related_manga,recommendations,studios,statistics','nsfw': True},
                            headers={'Authorization': f'Bearer {keys["access_token"]}'})
        end_time = time.time()
        latencies.append((end_time -start_time)*1000)
        ################
        # MAKE INSERT  #
        ################
        anime = res.json()
        anime_info = [anime['id'],anime['title'],anime['start_date'],anime['end_date'],anime['mean'],anime['popularity'],
                    anime['num_list_users'],anime['num_scoring_users'],anime['statistics']['status']['watching'],
                    anime['statistics']['status']['completed'],anime['statistics']['status']['on_hold'],anime['statistics']['status']['dropped'],
                    anime['statistics']['status']['plan_to_watch'],False if anime['nsfw'] == 'white' else True,anime['created_at'],
                    anime['updated_at'],media_lut.index(anime['media_type']),status_lut.index(anime['status_type']),anime['num_episodes'],
                    season_lut.index(anime['start season']['season']),anime['start season']['year'],source_lut.index(anime['source']),anime['average_episode_duration'],
                    rating_lut.index(anime['rating'])]
        print('anime info: ', anime_info)
        related_anime =[]
        for single_related_anime in anime['related_anime']:
            related_anime.append([anime['id'],single_related_anime['node']['id'],relation_lut.index(single_related_anime['node']['relation_type'])])

        recommended_anime =[]
        for single_recomended_anime in anime['recommendations']:
            recommended_anime.append([anime['id'],single_related_anime['node']['id'],single_recomended_anime['node']['num_recommendations']])

        recommended_anime =[]
        for single_recomended_anime in anime['recommendations']:
            recommended_anime.append([anime['id'],single_related_anime['node']['id'],single_recomended_anime['node']['num_recommendations']])
        anime_studios =[]
        for studio in anime['studios']:
            anime_studios.append()
        ###########
        # INSERT  #
        ###########
        cur.execute('''
                    INSERT INTO anime_info (
                        id, title, start_date, end_date, mean, rank, popularity,
                        num_list_users, num_scoring_users, num_watching_users,
                        num_completed_users, num_on_hold_users, num_dropped_users,
                        num_plan_to_watch_users, nsfw, created_at, updated_at,
                        media_id, status_id, num_episodes, start_season,
                        start_year, source_id, average_episode_duration, rating
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    );
                    ''',anime_info)
        
        cur.executemany('''
                    INSERT INTO related_anime
                    (original_id, related_id, related_type_id)
                    VALUES (?, ?, ?);
                    ''',related_anime)
        
        cur.executemany('''
                    INSERT INTO recommended_anime
                    (original_id, recommended_id, num_recommendations)
                    VALUES (?, ?, ?);
                    ''',recommended_anime)
        cur.executemany('''
                        INSERT INTO anime_studios
                        (id, studio_id)
                        VALUES (?, ?);
                        ''',)
        # except:
        #     pprint(res.json())
        #     raise Exception("The json that commited the crime")
        con.commit()
    return latencies


@timeit
def mine_100000_anime_by_ranking():
    #just good mining
    latencies = []
    for i in range(0,100000,500):
        print(12*'-')
        print("getting anime ", i,"-",i+499,"/100000")
        start_time = time.time()
        if i == 0:
            res = requests.get(base_url+'/anime/ranking', params={'ranking_type':'all','limit':500,'nsfw': True},
                            headers={'Authorization': f'Bearer {keys["access_token"]}'})
        else:
            res = requests.get(base_url+'/anime/ranking', params={'ranking_type':'all','limit':500,'offset':i,'nsfw': True},
                                headers={'Authorization': f'Bearer {keys["access_token"]}'})
        end_time = time.time()
        latencies.append((end_time -start_time)*1000)
        print(res.url)
        anime_info_json = res.json()['data']
        anime_info_list =[]
        for one_anime_data in anime_info_json:
            anime_info_list.append([one_anime_data['node']['id'],one_anime_data['node']['title'],one_anime_data['ranking']['rank']])
        if((num_anime:= len(anime_info_list)) == 0):
            break
        print("len of anime_list: ", num_anime)
        cur.executemany('INSERT INTO id_queue (id, title, ranking) VALUES(?, ?, ?)',anime_info_list)
        con.commit()
    return latencies

get_in_depth_info_for_each_anime()
# latencies = mine_100000_anime_by_ranking()
# plt.plot([i+1 for i in range(len(latencies))],latencies)
# plt.xlabel('Req Number (ms)')
# plt.ylabel('Latency')
# plt.show()
