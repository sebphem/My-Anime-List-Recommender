import requests
from pprint import pprint
import json
with open('keys/mal_token.json') as f:
    keys = json.load(f)

base_url = "https://api.myanimelist.net/v2"
res = requests.get(f'{base_url}/anime/{53246}', params={'fields':'id,title,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,num_episodes,start_season,broadcast,source,average_episode_duration,rating,related_anime,related_manga,recommendations,studios,statistics','nsfw': True},
                                headers={'Authorization': f'Bearer {keys["access_token"]}'})
pprint(res.json())
print(res.url)