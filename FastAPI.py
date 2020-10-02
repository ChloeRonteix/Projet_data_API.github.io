from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psycopg2
import psycopg2.extras
import sys
from film_infos import FilmInfo
from people_infos import PeopleInfo
import sql_script as ss
import helper
import uvicorn

app = FastAPI()
conn_string = "host='allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com'" "dbname='postgres'" "user='reader'" "password='reader'"
conn = psycopg2.connect(conn_string)
print(conn)

@app.get("/api/v2/films/film/{film_id}")
async def get_film_by_id(film_id:int):
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
    return helper.todict(film)

@app.get("/api/v2/people/{people_id}")
def get_people_by_id(people_id:int):
    cursor = conn.cursor()
    cursor.execute(ss.get_people_by_id, (people_id,))
    people = cursor.fetchone()
    p = PeopleInfo(people[2],people[1])
    p.id = people[0]
    return helper.todict(p)

@app.get('/api/v2/genres/all')
def get_all_genres():
    cursor = conn.cursor()
    cursor.execute(ss.get_all_genres)
    genres = cursor.fetchall()
    genres_list = []
    for genre in genres:
        genres_list.append(genre[0])
    return genres_list

@app.get('/api/v2/people/{people_id}/{role}/filmography')
def get_filmography(people_id:int, role:str):
    if role == None:
        return 'Please specify a role!', 500
    cursor = conn.cursor()
    if role == 'director':
        cursor.execute(ss.get_films_by_director, (people_id,))
    elif role == 'actor':
        cursor.execute(ss.get_films_by_actor, (people_id,))
    else:
        return 'Invalid role! Valid role are: [actor, director]'
    films = cursor.fetchall()
    films_titles = []
    for film in films:
        films_titles.append([film[0], film[1]])
    return films_titles

@app.get('/api/v2/genres/genre={genre}')
def get_films_by_genre(genre:str):
    cursor = conn.cursor()
    cursor.execute(ss.get_films_by_genre, (genre,))
    films = cursor.fetchall()
    films_titles = []
    for film in films:
        films_titles.append(film[0])
    return films_titles

@app.get('/api/v2/films/month') #nombre de films par mois
def get_count_films_by_month(): 
    cursor = conn.cursor()
    cursor.execute(ss.count_films_by_month)
    films_month = cursor.fetchall()
    list_films_month = []
    for film in films_month:
        list_films_month.append({'month': film[0], 'number_of_films': film[1]})
    headers = {'Access-Control-Allow-Origin':"*"}
    return JSONResponse(content=list_films_month, headers=headers)

@app.get('/api/v2/films/genres') #nombre de films par annnée
def get_count_films_by_genre(): #TODO add 'Access-Control-Allow-Origin'?
    cursor = conn.cursor()
    cursor.execute(ss.count_films_by_genre)
    films_genre = cursor.fetchall()
    list_films_genre = []
    for film in films_genre:
        list_films_genre.append({'genre': film[0], 'number_of_films': film[1]})
    headers = {'Access-Control-Allow-Origin':"*"}
    return JSONResponse(content=list_films_genre, headers=headers)

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8000)