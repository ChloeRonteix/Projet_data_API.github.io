import psycopg2
import sql_script as ss
from film_infos import FilmInfo

class PostgresFilmsRepository:

    def __init__(self):
        self.conn = psycopg2.connect(dbname="postgres", user="common", password="allocine", host="allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com")

    def add_film_to_postgres(self, film: FilmInfo):
        c = self.conn.cursor()
        try:
            c.execute(ss.insert_film, (film.id, film.title, film.date, film.synopsis, film.notes[0], film.notes[1]))
            self.conn.commit()
        except Exception as e:
            print(e)


    def add_genre_to_postgres(self, genres:list):
        c = self.conn.cursor()
        for g in genres:
            c.execute(ss.insert_genre, (g, g))
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