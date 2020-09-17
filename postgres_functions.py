import psycopg2
import sql_script as ss
from film_infos import FilmInfo

class PostgresFilmsRepository:

    def __init__(self):
        self.conn = psycopg2.connect(dbname="postgres", user="common", password="allocine", host="allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com")

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
    
    def get_last_page(self) -> int:
        #connection to database
        c = self.conn.cursor()
        try:
            c.execute(ss.get_last_scraped_page)
            return c.fetchone()[0]
        except Exception as e:
            print(e)
            return 0

    def save_page(self, page_id:int):
        c = self.conn.cursor()
        try:
            c.execute(ss.save_scraped_page, (page_id,))
            self.conn.commit()
        except Exception as e:
            print(e)