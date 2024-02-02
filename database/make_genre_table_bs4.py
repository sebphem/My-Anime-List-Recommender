from bs4 import BeautifulSoup
import requests
# https://myanimelist.net/anime/genre/3
genre_lut = []
i = 1
while True:
    try:
        res = requests.get(f'https://myanimelist.net/anime/genre/{i}')
        genre = BeautifulSoup(res.text,'html.parser').find('h1',{'class':'h1'}).text.strip()
    except Exception as err:
        print(res.text)
        print(err)
        break
    print(genre)
    genre_lut.append([i,genre.split(' ')[0]])
    if i % 10 == 0:
        print(genre_lut)
        if i > 81:
            break
    i+= 1

with open('genre_lut.txt') as f:
    f.write(str(genre_lut))