from configparser import ConfigParser
from pprint import pprint
from functools import wraps
from matplotlib import pyplot as plt
import os.path
import time
import requests
import json
from ip_switcher import switch_ip_address
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
    if switch_ip_address(0) is True:
        res = requests.get(base_url+'/anime/ranking', params={'ranking_type':'all','limit':500,'offset':500},
                        headers={'Authorization': f'Bearer {keys["access_token"]}'})
        print(res.url)
        return res.json()

def create_backup_id_queue():
    cur.execute('''
                CREATE TABLE IF NOT EXISTS id_queue_backup AS
                SELECT * FROM id_queue;''')
    con.commit()

def val_if_val_in_dict(anime, val: str):
    return anime[val] if val in anime else 'NA'

def lut_index_if_val_in_dict(lut : list, anime, val: str):
    return lut.index(anime[val]) if val in anime else 'NA'
@timeit
def get_in_depth_info_for_each_anime():
    #just good mining
    num_req_sent = 0
    empty_json_count = 0
    complete_json_count = 0
    time_out = 0.01
    relation_lut = ['sequel', 'prequel', 'alternative_setting', 'alternative_version', 'side_story', 'parent_story', 'summary', 'full_story','spin_off','other','character']
    source_lut = ['other', 'original', 'manga', '4_koma_manga', 'web_manga', 'digital_manga', 'novel', 'light_novel', 'visual_novel', 'game', 'card_game', 'book', 'picture_book', 'radio', 'music','web_novel','mixed_media']
    rating_lut = ['g', 'pg', 'pg_13', 'r', 'r+', 'rx']
    status_lut = ['finished_airing', 'currently_airing', 'not_yet_aired']
    media_lut = ['unknown', 'tv', 'ova', 'movie', 'special', 'ona', 'music','tv_special']
    season_lut = ['winter', 'spring','summer','fall']
    genre_lut = ['404','Action', 'Adventure', 'Racing', 'Comedy', 'Avant', 'Mythology', 'Mystery', 'Drama', 'Ecchi', 'Fantasy', 'Strategy', 'Hentai', 'Historical', 'Horror', 'Kids', '404', 'Martial', 'Mecha', 'Music', 'Parody', 'Samurai', 'Romance', 'School', 'Sci-Fi', 'Shoujo', 'Girls', 'Shounen', 'Boys', 'Space', 'Sports', 'Super', 'Vampire', '404', '404', 'Harem', 'Slice', 'Supernatural', 'Military', 'Detective', 'Psychological', 'Suspense', 'Seinen', 'Josei', '404', '404', 'Award', 'Gourmet', 'Workplace', 'Erotica', 'Adult', 'Anthropomorphic', 'CGDCT', 'Childcare', 'Combat', 'Delinquents', 'Educational', 'Gag', 'Gore', 'High', 'Idols', 'Idols', 'Isekai', 'Iyashikei', 'Love', 'Magical', 'Mahou', 'Medical', 'Organized', 'Otaku', 'Performing', 'Pets', 'Reincarnation', 'Reverse', 'Romantic', 'Showbiz', 'Survival', 'Team', 'Time', 'Video', 'Visual', 'Crossdressing']
    latencies = []

    #make session for the repeated requests
    ses = requests.Session()
    ses.headers.update({'Authorization': f'Bearer {keys["access_token"]}'})
    num_of_anime = cur.execute('SELECT COUNT(*) FROM id_queue WHERE status = "waiting"').fetchone()[0]

    print("num of anime: ", num_of_anime)
    print('anime name: ', )
    for i in range(0, num_of_anime, 1):
        # switch ips every 300 requests
        if num_req_sent%300 == 0:
            switch_ip_address(i//300)
            print('latencies:')
            for elem in latencies:
                print(elem)
        anime_q_tmp_val = cur.execute("SELECT id, title FROM id_queue WHERE status = 'waiting' ORDER BY ranking LIMIT 1").fetchone()
        if len(anime_q_tmp_val) == 0:
            print('this  is empty: ', anime_q_tmp_val,'\nso we\'re breaking the loop')
            break
        ###########
        # Console #
        ###########
        print(12*'-')
        print("getting anime ", i,"/",num_of_anime)
        print('anime name: ', anime_q_tmp_val[1])
        print('anime id: ', anime_q_tmp_val[0])
        ###########
        # Request #
        ###########
        while True:
            start_time = time.time()

            # res = requests.get(f'{base_url}/anime/{anime_q_tmp_val[0]}', params={'fields':'id,title,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,num_episodes,start_season,broadcast,source,average_episode_duration,rating,related_anime,related_manga,recommendations,studios,statistics','nsfw': True},
            #                        headers={'Authorization': f'Bearer {keys["access_token"]}'})

            # add id every time
            res = ses.get(f'https://api.myanimelist.net/v2/anime/{anime_q_tmp_val[0]}?fields=id%2Ctitle%2Cstart_date%2Cend_date%2Csynopsis%2Cmean%2Crank%2Cpopularity%2Cnum_list_users%2Cnum_scoring_users%2Cnsfw%2Ccreated_at%2Cupdated_at%2Cmedia_type%2Cstatus%2Cgenres%2Cnum_episodes%2Cstart_season%2Cbroadcast%2Csource%2Caverage_episode_duration%2Crating%2Crelated_anime%2Crelated_manga%2Crecommendations%2Cstudios%2Cstatistics&nsfw=True')

            status_code = res.status_code
            print('status code: ',status_code)
            end_time = time.time()
            print('latency with normal requests: ', end_time-start_time)
            latencies.append(end_time-start_time)
            #server is down, exponential delay on pinging it
            if status_code == 503:
                time_out *= 10
                print(f'server is down, wait {time_out}s')
                time.sleep(time_out)
            elif status_code > 400 and status_code < 410 :
                # print(res.url)
                print('status code: ', status_code)
                raise Exception('you messed up somewhere on the request')
            elif status_code == 200:
                # print(res.url)
                ################################
                # remove the exponential delay #
                ################################
                if time_out > 100:
                    time_out = 10
                time_out /= 10
                ################
                # MAKE JSON  #
                ################
                try:
                    anime = res.json()
                except:
                    print('something can\'t be serialized in this text: ', res.text)
                #################
                if anime['id'] <= 0:
                    print('anime id: ', anime['id'])
                    print('getting the id less than 1 error, trying again')
                elif len(anime) != 0:
                    complete_json_count += 1
                    break
                else:
                    print('the json is empty, trying again')
                    print(res)
                    empty_json_count += 1
                    print(f'json accuracy: {complete_json_count}/{complete_json_count+empty_json_count}')
        # latencies.append((end_time -start_time)*1000)
        try:
            #make the data null if not in the dict
            try:
                stats_status = anime['statistics']['status']
            except:
                stats_status = {}

            ########################
            # Make the data vector #
            ########################
            # account for all potential loss of data
            anime_info = [anime['id'],anime['title'],val_if_val_in_dict(anime,'start_date'),val_if_val_in_dict(anime,'end_date'),val_if_val_in_dict(anime,'mean'),val_if_val_in_dict(anime,'rank'),val_if_val_in_dict(anime,'popularity'), val_if_val_in_dict(anime,'num_list_users'),val_if_val_in_dict(anime,'num_scoring_users'),
                        val_if_val_in_dict(stats_status,'watching'), val_if_val_in_dict(stats_status,'completed'),val_if_val_in_dict(stats_status,'on_hold'),val_if_val_in_dict(stats_status,'dropped'),val_if_val_in_dict(stats_status,'plan_to_watch'),
                        False if val_if_val_in_dict(anime,'nsfw') == 'white' else True,
                        val_if_val_in_dict(anime,'created_at'), val_if_val_in_dict(anime,'updated_at'),
                        lut_index_if_val_in_dict(media_lut,anime,'media_type'), lut_index_if_val_in_dict(status_lut,anime,'status'),
                        val_if_val_in_dict(anime,'num_episodes'),
                        lut_index_if_val_in_dict(season_lut, anime['start_season'], 'season') if 'start_season' in anime else 'NA',
                        val_if_val_in_dict( anime['start_season'], 'year') if 'start_season' in anime else 'NA',
                        lut_index_if_val_in_dict(source_lut, anime, 'source'), val_if_val_in_dict(anime,'average_episode_duration'), lut_index_if_val_in_dict(rating_lut, anime, 'rating')]
        except Exception as err:
            pprint(anime)
            raise err
        # print('anime info: ', anime_info)
        related_anime =[]
        for single_related_anime in anime['related_anime']:
            related_anime.append([anime['id'],single_related_anime['node']['id'],relation_lut.index(single_related_anime['relation_type'])])

        recommended_anime =[]
        for single_recomended_anime in anime['recommendations']:
            # print('single rec\'d anime: ', single_recomended_anime)
            recommended_anime.append([anime['id'],single_recomended_anime['node']['id'],single_recomended_anime['num_recommendations']])

        if 'genres' in anime:
            anime_genres =[]
            for genre in anime['genres']:
                anime_genres.append([anime['id'],genre['id']])
        if 'studios' in anime:
            anime_studios =[]
            for studio in anime['studios']:
                anime_studios.append([anime['id'],studio['id']])

        ###########
        # INSERT  #
        ###########
        cur.execute('''
                    INSERT INTO anime_info (
                        id, title, start_date, end_date, mean, rank, popularity, num_list_users, num_scoring_users,
                        num_watching_users, num_completed_users, num_on_hold_users, num_dropped_users, num_plan_to_watch_users,
                        nsfw,
                        created_at, updated_at,
                        media_id, status_id,
                        num_episodes,
                        start_season,
                        start_year,
                        source_id, average_episode_duration, rating
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    );
                    ''',anime_info)

        cur.execute('''
                        INSERT INTO anime_synopsis
                        (id, synopsis)
                        VALUES (?, ?);
                        ''',[anime['id'],anime['synopsis']])
        
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
                        ''',anime_studios)
        # except:
        #     pprint(res.json())
        #     raise Exception("The json that commited the crime")
        cur.execute('''UPDATE id_queue
                    SET status = 'done'
                    WHERE id = ?
                    ''',[anime_q_tmp_val[0]])
        con.commit()
        num_req_sent += 1
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
# test_anime_ranking()
get_in_depth_info_for_each_anime()
# latencies = mine_100000_anime_by_ranking()
# plt.plot([i+1 for i in range(len(latencies))],latencies)
# plt.xlabel('Req Number (ms)')
# plt.ylabel('Latency')
# plt.show()
