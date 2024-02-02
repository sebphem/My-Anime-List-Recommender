from bs4 import BeautifulSoup
import requests
# https://myanimelist.net/anime/genre/
genre_lut = []
i = 1
while True:
    try:
        res = requests.get(f'https://myanimelist.net/anime/producer/{i}')
        genre = BeautifulSoup(res.text,'html.parser').find('h1',{'class':'title-name'}).text.strip()
    except Exception as err:
        genre = BeautifulSoup(res.text,'html.parser').find('p',{'class':'message'}).text.strip()
        if genre == "This page doesn't exist.":
            genre = '404'
        else:
            print(err)
            break
    print(genre)
    genre_lut.append([i,genre])
    if i % 10 == 0:
        print(genre_lut)
    i+= 1

with open('./producer_lut.txt','w') as f:
    f.write(str(genre_lut))