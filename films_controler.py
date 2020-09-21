import flask
from flask import request, jsonify
import psycopg2
import psycopg2.extras
import sys
from film_infos import FilmInfo
from people_infos import PeopleInfo

app = flask.Flask(__name__)
app.config["DEBUG"] = True
conn_string = "host='allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com'" "dbname='postgres'" "user='common'" "password='allocine'" 
conn = psycopg2.connect(conn_string)

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn_string = "host='allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com'" "dbname='postgres'" "user='common'" "password='allocine'" 
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM films LIMIT 50')
    all_movies = cursor.fetchall()

    return jsonify(all_movies)

@app.route('/api/v1/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id:int):
    cursor = conn.cursor()
    cursor.execute('SELECT id, provider_id, title, date, synopsis, note_press, note_people FROM films WHERE id = %s', (film_id,))
    movie = cursor.fetchone()
    film = FilmInfo()
    film.id = movie[0]
    film.provider_id = movie[1]
    film.title = movie[2]
    film.date = movie[3]
    film.synopsis = movie[4]
    film.notes = (movie[5],movie[6])
    cursor.execute('SELECT g.name from genres g JOIN films_genres fg ON g.id = fg.id_genre WHERE fg.id_film = %s;', (film_id,))
    genres = cursor.fetchall()
    for genre in genres:
        film.genres.append(genre[0])
    cursor.execute('SELECT p.full_name from people p JOIN films_actors fa ON p.id = fa.id_actor WHERE fa.id_film = %s', (film_id,))
    actors = cursor.fetchall()
    for actor in actors:
        people = PeopleInfo(actor[0],None)
        film.actors.append(people)
    return film.toJSON()


app.run()