import requests
import bs4
import time
import pandas as pd
from film_infos import FilmInfo
from datetime import date
from people_infos import PeopleInfo
import psycopg2
from postgres_functions import PostgresFilmsRepository


base_url = 'http://www.allocine.fr/films/?page='

#conn = psycopg2.connect(dbname="postgres", user="common", password="allocine", host="allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com")
pf = PostgresFilmsRepository()


def start_scrap():
    #df = pd.DataFrame(columns=('title', 'id', 'actors', 'directors', 'date', 'genres', 'synopsis', 'notes_presse','note_spec'))
    last_scraped_page = pf.get_last_page()
    for i in range(last_scraped_page+1, last_scraped_page+11):
        boxes = get_films_box(i)
        for box in boxes:
            film = get_filmInfos(box)
            #df = add_to_df(film,df)
            add_to_postgres(film)
        print(f'Page {i} scrapped!')
        pf.save_page(i)
        print(f'Page {i} saved!')
        time.sleep(1)
    #print(df)
    #print(df['date'])
    #print(df['directors'])
    #print(df['genres'])


def add_to_df(film: FilmInfo, data):
    return data.append(film.to_dictionary(), ignore_index=True)

def add_to_postgres(film: FilmInfo): 
    film_id = pf.add_film_to_postgres(film)
    pf.add_genre_to_postgres(film.genres, film_id)
    pf.add_actor_to_postgres(film.actors, film_id)
    pf.add_director_to_postgres(film.director, film_id)

def get_films_box(pages_index: int):
    url = base_url + str(pages_index)
    response = requests.get(url)
    print(response)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    film_boxes = soup.find_all("div", {"class":"entity-card-list"})
    return film_boxes

def get_title(film):
    title_url = film.find("a", {"class":"meta-title-link"})
    title = title_url.text
    return title

def get_id(film):
    title_url = film.find("a", {"class":"meta-title-link"})
    url = title_url['href']
    start = url.index('=')+1
    end = url.index('.')
    id_film = int(url[start:end])
    return id_film

def get_actors(film):
    actors = []
    actors_bloc = film.find('div', {'class':'meta-body-actor'})
    if actors_bloc != None:
        actors_div = actors_bloc.find_all(["a","span"], class_=(lambda x: x != 'light'))
        for acteur in actors_div:
            id_actor = None
            if acteur.name == "a":
                url = acteur['href']
                start = url.index('=')+1
                end = url.index('.')
                id_actor = int(url[start:end])
            actor_info = PeopleInfo(acteur.text, id_actor)
            #print(actor_info.id, actor_info.full_name)
            actors.append(actor_info)
    return actors

def get_styles(film):
    meta_body_info = film.find("div", {"class":"meta-body-info"})
    genres_film = meta_body_info.find_all("span", class_=lambda x: x != 'date' and x != 'spacer')
    genres =[]
    for genre in genres_film:
        genres.append(genre.text)
    return genres

def get_date(film): #TODO: convert date
    months = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
    date_div = film.find('span', {'class':'date'})
    if date_div == None:
        return None
    date_part = date_div.text.split()
    if len(date_part) == 1:
        film_date = date(int(date_part[0]), 1, 1)
    else:
        month_id = months.index(date_part[1])+1
        film_date = date(int(date_part[2]), month_id, int(date_part[0]))
    return film_date # Voir dateparser.parse(date_string).date()

def get_real(film): #TODO: get id provider
    real = film.find_all("a", {"class":"blue-link"})
    realisateurs = []
    for realisateur in real:
        id_real = None
        if realisateur.name == "a":
            url = realisateur['href']
            start = url.index('=')+1
            end = url.index('.')
            id_real = int(url[start:end])
        director_info = PeopleInfo(realisateur.text, id_real)
        realisateurs.append(director_info)
    return realisateurs

def get_synopsis(film):
    synops = film.find("div", {"class":"content-txt"})
    if synops == None:
        return None
    return synops.text.strip()

def get_notes(film):
    note_presse = 0.0
    note_spec = 0.0
    evaluation = film.find('div', {'class':'rating-holder'})
    if evaluation == None:
        return (None,None)
    notes_div = evaluation.find_all('div', {'class':'rating-item-content'})
    for note in notes_div:
        note_float = None
        note_value = note.find('span', {'class': 'stareval-note'}).text
        if note_value != '--':
            note_float = float(note_value.replace(',', '.'))
        if "Spectateurs" in note.text:
            note_spec = note_float
        elif "Presse" in note.text:
            note_presse = note_float
    return(note_presse, note_spec)

def get_filmInfos(box) -> FilmInfo:
    film = FilmInfo()
    film.provider_id = get_id(box)
    film.title = get_title(box)
    film.director = get_real(box)
    film.actors = get_actors(box)
    film.synopsis = get_synopsis(box)
    film.notes = get_notes(box)
    film.date = get_date(box)
    film.genres = get_styles(box)
    return film


#DEBUT SCRAPING
start_scrap()

#FIN SCRAPING
print("FINI")

