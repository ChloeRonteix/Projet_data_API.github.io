import psycopg2
import sql_script as ss

class PostgresFilmsRepository:

    def __init__(self):
        self.conn = psycopg2.connect(dbname="postgres", user="common", password="allocine", host="allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com")

    def add_film_to_postgres(self):
        c = self.conn.cursor()
        try:
            c.execute(ss.insert_film, (film.id, film.title, film.date, film.synopsis, film.notes[0], film.notes[1]))
            self.conn.commit()
        except Exception as e:
            print(e)


    def add_genre_to_postgres(self, genre):
        for g in genre:
            c.execute(ss.insert_genre, (g, g))
            conn.commit()