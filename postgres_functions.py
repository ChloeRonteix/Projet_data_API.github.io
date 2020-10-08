import psycopg2
import sql_script as ss
from film_infos import FilmInfo
from people_infos import PeopleInfo
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")

class PostgresFilmsRepository:

    def __init__(self):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

    def add_film_to_postgres(self, film: FilmInfo) -> int:
        c = self.conn.cursor()
        c.execute(ss.get_film_id_by_provider_id, (film.provider_id,))
        fetched = c.fetchone()
        if fetched == None:
            try:
                c.execute(ss.insert_film, (film.provider_id, film.title, film.date, film.synopsis, film.notes[0], film.notes[1]))
                film_id = c.fetchone()[0]
            except Exception as e:
                print(e)
            self.conn.commit()
        else:
            film_id = fetched[0]
        return film_id


    def add_genre_to_postgres(self, genres:list, film_id:int):
        c = self.conn.cursor()
        for g in genres:
            c.execute(ss.get_genre_id_by_name, (g,))
            fetched = c.fetchone()
            if fetched == None:
                try:
                    c.execute(ss.insert_genre, (g,))
                    genre_id = c.fetchone()[0]
                except Exception as e:
                    print(e)
                self.conn.commit()
            else:
                genre_id = fetched[0]
            try:
                c.execute(ss.insert_genre_for_film, (film_id, genre_id))
            except Exception as e:
                print(e)
            self.conn.commit()
    
    def add_actor_to_postgres(self, actors:list, film_id:int):
        c = self.conn.cursor()
        for a in actors:
            c.execute(ss.get_people_by_name, (a.full_name,))
            fetched = c.fetchone()
            if fetched == None:
                try:
                    c.execute(ss.insert_people, (a.full_name, a.provider_id))
                    actor_id = c.fetchone()[0]
                except Exception as e:
                    print(e)
                self.conn.commit()
            else:
                actor_id = fetched[0]
                if fetched[1] == None and a.provider_id != None:
                    c.execute(ss.update_provider_id, (a.provider_id,actor_id))
            try:
                c.execute(ss.insert_actor_for_film, (film_id, actor_id))
            except Exception as e:
                print(e)
            self.conn.commit()

    def add_director_to_postgres(self, realisateurs:list, film_id:int):
        c = self.conn.cursor()
        for r in realisateurs:
            c.execute(ss.get_people_by_name, (r.full_name,))
            fetched = c.fetchone()
            if fetched == None:
                try:
                    c.execute(ss.insert_people, (r.full_name, r.provider_id))
                    director_id = c.fetchone()[0]
                except Exception as e:
                    print(e)
                self.conn.commit()
            else:
                director_id = fetched[0]
                if fetched[1] == None and r.provider_id != None:
                    c.execute(ss.update_provider_id, (r.provider_id,director_id))
            try:
                c.execute(ss.insert_director_for_film, (film_id, director_id))
            except Exception as e:
                print(e)
            self.conn.commit()
    
    
    def get_last_page(self) -> int:
        #connection to database
        c = self.conn.cursor()
        try:
            c.execute(ss.get_last_scraped_page)
            return c.fetchone()[0]
        except:
            print('Last page not found')
            return 0

    def save_page(self, page_id:int):
        c = self.conn.cursor()
        try:
            c.execute(ss.save_scraped_page, (page_id,))
            self.conn.commit()
        except Exception as e:
            print(e)