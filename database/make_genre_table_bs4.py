from bs4 import BeautifulSoup
import requests
import sqlite3
def webscrape_genre_info():
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

def insert_into_genre_table(big_array):
    for elem in big_array:
        if elem[1] == '404':
            elem[1] = 'NA'
    con = sqlite3.connect('./mal.db')
    cur = con.cursor()
    cur.executemany('''
                    INSERT INTO genre_lut
                    (genre_id, genre_name)
                    VALUES (?, ?);
                    ''',big_array)
    con.commit()
big_array = [[1, 'Action'], [2, 'Adventure'], [3, 'Racing'], [4, 'Comedy'], [5, 'Avant'], [6, 'Mythology'], [7, 'Mystery'], [8, 'Drama'], [9, 'Ecchi'], [10, 'Fantasy'], [11, 'Strategy'], [12, 'Hentai'], [13, 'Historical'], [14, 'Horror'], [15, 'Kids'], [16, '404'], [17, 'Martial'], [18, 'Mecha'], [19, 'Music'], [20, 'Parody'], [21, 'Samurai'], [22, 'Romance'], [23, 'School'], [24, 'Sci-Fi'], [25, 'Shoujo'], [26, 'Girls'], [27, 'Shounen'], [28, 'Boys'], [29, 'Space'], [30, 'Sports'], [31, 'Super'], [32, 'Vampire'], [33, '404'], [34, '404'], [35, 'Harem'], [36, 'Slice'], [37, 'Supernatural'], [38, 'Military'], [39, 'Detective'], [40, 'Psychological'], [41, 'Suspense'], [42, 'Seinen'], [43, 'Josei'], [44, '404'], [45, '404'], [46, 'Award'], [47, 'Gourmet'], [48, 'Workplace'], [49, 'Erotica'], [50, 'Adult'], [51, 'Anthropomorphic'], [52, 'CGDCT'], [53, 'Childcare'], [54, 'Combat'], [55, 'Delinquents'], [56, 'Educational'], [57, 'Gag'], [58, 'Gore'], [59, 'High'], [60, 'Idols'], [61, 'Idols'], [62, 'Isekai'], [63, 'Iyashikei'], [64, 'Love'], [65, 'Magical'], [66, 'Mahou'], [67, 'Medical'], [68, 'Organized'], [69, 'Otaku'], [70, 'Performing'], [71, 'Pets'], [72, 'Reincarnation'], [73, 'Reverse'], [74, 'Romantic'], [75, 'Showbiz'], [76, 'Survival'], [77, 'Team'], [78, 'Time'], [79, 'Video'], [80, 'Visual'], [81, 'Crossdressing']]
insert_into_genre_table(big_array)