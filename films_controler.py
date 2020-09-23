import flask
from flask import request, jsonify
import psycopg2
import psycopg2.extras
import sys
from film_infos import FilmInfo
from people_infos import PeopleInfo
import sql_script as ss

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
    cursor.execute(ss.get_film_by_id, (film_id,))
    movie = cursor.fetchone()
    film = FilmInfo()
    film.id = movie[0]
    film.provider_id = movie[1]
    film.title = movie[2]
    film.date = movie[3]
    film.synopsis = movie[4]
    film.notes = (movie[5],movie[6])
    cursor.execute(ss.get_genres_film, (film_id,))
    genres = cursor.fetchall()
    for genre in genres:
        film.genres.append(genre[0])
    cursor.execute(ss.get_actors_by_film, (film_id,))
    actors = cursor.fetchall()
    for actor in actors:
        people = PeopleInfo(actor[0],None)
        film.actors.append(people)
    cursor.execute(ss.get_directors_by_film, (film_id,))
    directors = cursor.fetchall()
    for director in directors:
        people = PeopleInfo(director[0],None)
        film.director.append(people)
    return film.toJSON()

@app.route('/api/v1/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id:int):
    cursor = conn.cursor()
    cursor.execute(ss.get_people_by_id, (people_id,))
    people = cursor.fetchone()
    p = PeopleInfo(people[2],people[1])
    p.id = people[0] 
    return p.toJSON()

@app.route('/api/v1/people/<int:people_id>/film_actor', methods=['GET'])
def get_films_by_id_actor(people_id:int):
    cursor = conn.cursor() 
    cursor.execute(ss.get_films_by_actor, (people_id,))
    films = cursor.fetchall()
    films_titles = []
    for film in films:
        films_titles.append(film[0])
    return jsonify(films_titles)

@app.route('/api/v1/people/<int:people_id>/film_director', methods=['GET'])
def get_films_by_id_director(people_id:int):
    cursor = conn.cursor() 
    cursor.execute(ss.get_films_by_director, (people_id,))
    films = cursor.fetchall()
    films_titles = []
    for film in films:
        films_titles.append(film[0])
    return jsonify(films_titles)
    
@app.route('/api/v1/people/<int:people_id>/filmography', methods=['GET']) #route avec query parameter
def get_filmography(people_id:int):
    role = request.args.get('role')
    cursor = conn.cursor()
    if role == 'director':
        cursor.execute(ss.get_films_by_director, (people_id,))
    elif role == 'actor':
        cursor.execute(ss.get_films_by_actor, (people_id,))
    films = cursor.fetchall()
    films_titles = []
    for film in films:
        films_titles.append(film[0])
    return jsonify(films_titles)

@app.route('/api/v1/genres/all', methods=['GET'])
def get_all_genres():
    cursor = conn.cursor() 
    cursor.execute(ss.get_all_genres)
    genres = cursor.fetchall()
    genres_list = []
    for genre in genres:
        genres_list.append(genre)
    return jsonify(genres_list)

@app.route('/api/v1/genres/<int:genre_id>', methods=['GET'])
def get_genre_by_id(genre_id:int):
    cursor = conn.cursor() 
    cursor.execute(ss.get_genre_by_id, (genre_id,))
    genre = cursor.fetchone()
    return jsonify(genre)

#TODO: route films selon l'id du genre

app.run()