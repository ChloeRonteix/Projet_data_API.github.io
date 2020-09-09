import requests
import bs4
import time
import pandas as pd
from film_infos import FilmInfo

base_url = 'http://www.allocine.fr/films/?page='
df = pd.DataFrame(columns=('titre', 'id', 'acteurs', 'realisateur', 'date de sortie', 'genres', 'synopsis', 'note'))

scrap = start_scrap()

def start_scrap():
    last_scraped_page = 0
    for i in range(last_scraped_page+1, last_scraped_page+3):
        boxes = get_films_box(i)
        for box in boxes:
            film = FilmInfo()
            film.id = get_id(box)
            film.titre = get_title(box)
            film.director = get_real(box)
            film.actors = get_actors(box)
            film.synopsis = get_synopsis(box)
            film.notes = get_notes(box)
            film.date = get_date(box)
        time.sleep(5)

def add_to_df(film: FilmInfo): #TODO: fonction pour envoyer vers df
    df = df.append(film.to_dictionary(), ignore_index=True)

def add_to_postgre(film: FilmInfo): #TODO: fonction pour envoyer vers db
    pass


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
    actors_film = film.find('div', {'class':'meta-body-actor'})
    for acteurs in actors_film:
        acteurs = acteur.find_all(["a","span"], class_=(lambda x: x != 'light'))
        for acteur in acteurs:
            actors.append(acteur.text)
    return actors

def get_styles(film):
    meta_body_info = film.find("div", {"class":"meta-body-info"})
    genres_film = meta_body_info.find_all("span", class_=lambda x: x != 'date' and x != 'spacer')
    genres =[]
    for genre in genres_film:
        genres.append(genre.text)
    return genres

def get_date(film): #TODO: convert date
    date = film.find('span', {'class':'date'}).text
    return date # Voir dateparser.parse(date_string).date()

def get_real(film):
    real = film.find_all("a", {"class":"blue-link"})
    realisateurs = []
    for realisateur in real:
        realisateurs.append(realisateur.text)
    return realisateurs

def get_synopsis(film): #TODO: à retravailler
    synops = film.find_all("div", {"class":"content-txt"})
    synopsis=[]
    synopsis_clean=[]
    for i in synops:
        synopsis.append(i.text)
    for i in synopsis:
        synopsis_clean.append((" ".join(i.split())))
    return synopsis_clean

def get_notes(film):
    note_presse = 0.0
    note_spec = 0.0
    evaluation = film.find_all('div', {'class':'rating-holder'})
    if len(evaluation) != 0:
        for rating in evaluation:
            notes = rating.find_all('span', {'class': 'stareval-note'})
            note_presse += float((notes[0].text).replace(',', '.'))
            note_spec += float((notes[1].text).replace(',', '.'))
    return(note_presse, note_spec)

def get_id_actor(film):
    pass

#TODO: script de scrap with function



print("FINI")

print(df)