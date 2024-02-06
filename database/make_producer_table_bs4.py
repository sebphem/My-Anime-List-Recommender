from bs4 import BeautifulSoup
import requests
import sqlite3
# https://myanimelist.net/anime/genre/
def webscrape_producer_info():
    genre_lut = []
    i = 2131
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
    return genre_lut

#because the mining was done in parts, we need to join the files together
def make_one_big_array(write_to_array : list,*read_from_array):
    for elem in read_from_array:
        write_to_array.append(elem)
    return write_to_array

def make_lookup_array(big_array):
    lookup_array = ['']
    for elem in big_array:
        print(len(elem))
        if len(big_array) == elem[0]:
            lookup_array.append(elem[1])
        else:
            lookup_array.insert(elem[0],elem[1])
    return lookup_array

def insert_into_producer_table(big_array):
    for elem in big_array:
        if elem[1] == '404':
            elem[1] = 'NA'
    con = sqlite3.connect('./mal.db')
    cur = con.cursor()
    cur.executemany('''INSERT INTO studio_lut
                    (studio_id, studio_name)
                    VALUES (?, ?);''',
                    big_array)
    con.commit()

# insert_into_producer_table(big_array)