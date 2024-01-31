from configparser import ConfigParser
import requests
config = ConfigParser()
config.read('keys/config.ini')
print(config.sections())

print(config['mal']['CLIENT_ID'])
client_secret = config['mal']['BEARER']

base_url = "https://api.myanimelist.net/v2"


res = requests.get(base_url+'/anime', params={'q':'one','limit':4},
                   headers={'Authorization': f'Bearer {client_secret}'})
print(res.url)
print(res.json())