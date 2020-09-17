import psycopg2

class Postgres:

    def __init__(self):
        self.conn = psycopg2.connect(dbname="postgres", user="common", password="allocine", host="allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com")
        self.c = self.conn.cursor()

    def add_film_to_postgres():
        try:
            self.c.execute(ss.insert_film, (film.id, film.title, film.date, film.synopsis, film.notes[0], film.notes[1]))
            self.conn.commit()
        except Exception as e:
            print(e)


    def add_genre_to_postgres(genre):
        for g in genre:
            c.execute(ss.insert_genre, (g, g))
            conn.commit()