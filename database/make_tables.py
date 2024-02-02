import sqlite3
import os.path
con = sqlite3.connect(os.path.dirname(__file__) +'/mal.db')
cur = con.cursor()

def make_info_queue():
    # Because anime ranking only holds basic data, make a queue to find out more information
    # https://myanimelist.net/apiconfig/references/api/v2#operation/anime_ranking_get
    cur.executescript('''
                CREATE TABLE IF NOT EXISTS id_queue(
                    id int UNIQUE,
                    title string,
                    ranking int,
                    PRIMARY KEY (id)
                );
                ''')
    con.commit()
    print(cur.execute('SELECT * FROM id_queue;').fetchall())
    

#This can be optimized, but I need to be able to tweak the individual tables
def make_anime_info_table():
    #store most of the information
    #https://myanimelist.net/apiconfig/references/api/v2#operation/anime_anime_id_get
    cur.executescript('''
                    DROP TABLE IF EXISTS anime_info;
                    CREATE TABLE anime_info(
                        id int UNIQUE,
                        title string,
                        start_date string,
                        end_date string,
                        mean float,
                        rank int,
                        popularity int,
                        num_list_users int,
                        num_scoring_users int,
                        num_watching_users int,
                        num_completed_users int,
                        num_on_hold_users int,
                        num_dropped_users int,
                        num_plan_to_watch_users int,
                        nsfw bool,
                        created_at string,
                        updated_at string,
                        media_id int,
                        status_id int,
                        num_episodes int,
                        start_season int,
                        start_year int,
                        source_id int,
                        average_episode_duration int,
                        rating int,
                        PRIMARY KEY (id)
                    );
                    ''')
    
    cur.executescript('''
                    DROP TABLE IF EXISTS related_anime;
                    CREATE TABLE related_anime(
                        original_id int,
                        related_id int,
                        related_type_id int,
                        PRIMARY KEY(original_id)
                    );
                    ''')

    cur.executescript('''
                    DROP TABLE IF EXISTS recommended_anime;
                    CREATE TABLE recommended_anime(
                        original_id int,
                        recommended_id int,
                        num_recommendations int,
                        PRIMARY KEY(original_id)
                    );
                    ''')
    cur.executescript('''
                    DROP TABLE IF EXISTS anime_synopsis;
                    CREATE TABLE anime_synopsis(
                        id int,
                        synopsis string,
                        PRIMARY KEY(id)
                    );
                    ''')
    
    cur.executescript('''
                    DROP TABLE IF EXISTS anime_genre;
                    CREATE TABLE genre_info(
                        id int,
                        genre_id int,
                        PRIMARY KEY (id)
                    );
                    ''')
    cur.executescript('''
                    DROP TABLE IF EXISTS anime_studios;
                    CREATE TABLE anime_studios(
                        id int,
                        studio_id int,
                        PRIMARY KEY (id)
                    );
                    ''')
    con.commit()

def make_lookup_tables():
    cur.executescript('''
                DROP TABLE IF EXISTS genre_lut;
                CREATE TABLE genre_lut(
                    genre_id int UNIQUE,
                    genre_name string,
                    PRIMARY KEY (genre_id)
                );
                CREATE TABLE IF NOT EXISTS studio_lut(
                    studio_id int UNIQUE,
                    studio_name string UNIQUE,
                    PRIMARY KEY (studio_id)
                );
                CREATE TABLE IF NOT EXISTS media_lut(
                    media_id int UNIQUE,
                    media_name string UNIQUE,
                    PRIMARY KEY (media_id)
                );
                CREATE TABLE IF NOT EXISTS status_lut(
                    status_id int UNIQUE,
                    status_name string,
                    PRIMARY KEY (status_id)
                );
                CREATE TABLE IF NOT EXISTS rating_lut(
                    rating_id int UNIQUE,
                    rating_name string,
                    PRIMARY KEY (rating_id)
                );
                CREATE TABLE IF NOT EXISTS source_lut(
                    source_id int UNIQUE,
                    source_name string,
                    PRIMARY KEY (source_id)
                );
                CREATE TABLE IF NOT EXISTS relation_lut(
                    related_type_id int UNIQUE,
                    relation_name string,
                    PRIMARY KEY (related_type_id)
                );
                ''')
    try:
        cur.executemany('''
                    INSERT INTO genre_lut (genre_id,genre_name) VALUES(?,?)''',
                    [[1,'Action'],[2,'Adventure'],[5,'Avant Garde'],[46,'Award Winning'],[28,'Boys Love'],[4,'Comedy'],[8,'Drama'],
                     [10,'Fantasy'],[26,'Girls Love'],[47,'Gourmet'],[14,'Horror'],[7,'Mystery'],[22,'Romance'],[24,'Sci-fi'],
                     [30,'Sports'],[36,'Slice of Life'][37,'Supernatural'],[41,'Suspense'],[9,'Ecchi'],[49,'Erotica'],[12,'Hentai'],[50,'Adult Cast'],
                     [51,'Antropomorphic'],[52,'CGDCT'],[53,'Childcare'],[54,'Combat Sports'],[55,'Delinquents'],[39,'Detective'],[56,'Educational'],[57,'Gag Humor'],[58,'Gore'],
                     [35,'Harem'],[59,'High Stakes Game'],[13,'Historical'],[60,'Idols (Female)'],[61,'Idols (Male)'],[62,'Isekai'],[63,'Iyashikei'],[64,'Love Polygon'],
                     [65,'Magical Sex Shift'],[66,'Mahou Shoujo'],[17, 'Martial Arts'],[18,'Mecha'],[67,'Medical'],[38,'Military'],[19,'Music'],[6,'Mythology'],
                     ])
        #['unknown', 'tv', 'ova', 'movie', 'special', 'ona', 'music']
        #list_name.index('unknown')
    except:
        pass
    try:
        cur.executemany('''
                    INSERT INTO media_lut (media_id,media_name) VALUES(?,?)''',
                    [[0,'unknown'],[1,'tv'],[2,'ova'],[3,'movie'],[4,'special'],[5,'ona'],[6,'music']])
        #['unknown', 'tv', 'ova', 'movie', 'special', 'ona', 'music']
        #list_name.index('unknown')
    except:
        pass
    try:
        cur.executemany('''
                    INSERT INTO status_lut (status_id,status_name) VALUES(?,?)''',
                    [[0,'finished_airing'],[1,'currently_airing'],[2,'not_yet_aired']])
        #['finished_airing', 'currently_airing', 'not_yet_aired']
    except:
        pass
    try:
        cur.executemany('''
                    INSERT INTO rating_lut (rating_id,rating_name) VALUES(?,?)''',
                    [[0, 'g'], [1, 'pg'], [2, 'pg_13'], [3, 'r'], [4, 'r+'], [5, 'Hentai']])
        #['g', 'pg', 'pg_13', 'r', 'r+', 'Hentai']
    except:
        pass
    try:
        cur.executemany('''
                    INSERT INTO source_lut (source_id,source_name) VALUES(?,?)''',
                    [[0, 'other'], [1, 'original'], [2, 'manga'], [3, '4_koma_manga'], [4, 'web_manga'], [5, 'digital_manga'], [6, 'novel'], [7, 'light_novel'], [8, 'visual_novel'], [9, 'game'], [10, 'card_game'], [11, 'book'], [12, 'picture_book'], [13, 'radio'], [14, 'music']])
        #['other', 'original', 'manga', '4_koma_manga', 'web_manga', 'digital_manga', 'novel', 'light_novel', 'visual_novel', 'game', 'card_game', 'book', 'picture_book', 'radio', 'music']
    except:
        pass
    try:
        cur.executemany('''
                    INSERT INTO relation_lut (related_type_id,relation_name) VALUES(?,?)''',
                    [[0, 'sequel'], [1, 'prequel'], [2, 'alternative_setting'], [3, 'alternative_version'], [4, 'side_story'], [5, 'parent_story'], [6, 'summary'], [7, 'full_story']])
        #['sequel', 'prequel', 'alternative_setting', 'alternative_version', 'side_story', 'parent_story', 'summary', 'full_story']
    except:
        pass
    con.commit()

make_info_queue()
make_lookup_tables()
make_anime_info_table()