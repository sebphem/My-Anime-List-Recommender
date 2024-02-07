import requests
import json

with open('./../keys/keys.json') as f:
    keys = json.load(f)

id=

ses = requests.Session()
ses.headers({'Authorization': f'Bearer {keys["access_token"]}'})
res = ses.get(f'{base_url}/anime/{id}',params={'fields':'id,title,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,num_episodes,start_season,broadcast,source,average_episode_duration,rating,related_anime,related_manga,recommendations,studios,statistics','nsfw': True})