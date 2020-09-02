import bs4
import requests
import pandas as pd


response = requests.get('http://www.allocine.fr/films/')

soup = bs4.BeautifulSoup(response.text, 'html.parser')
#print(soup)
em_box = soup.find_all("div", {"class":"entity-card-list"})
print(len(em_box))

df = pd.DataFrame(columns=('titre', 'id', 'acteurs', 'realisateur', 'date de sortie', 'genres', 'synopsis'))

for film in em_box:
    # Titre
    title_url = film.find("a", {"class":"meta-title-link"})
    title = title_url.text
    #print(title)
    #Id du film
    url = title_url['href']
    start = url.index('=')+1
    end = url.index('.')
    id_film = int(url[start:end])
    #print(id_film)
    #Acteurs
    actors = film.find('div', {'class':'meta-body-actor'})
    acteur_clean = []
    acteur_clean.append((" ".join(actors.text.split()).replace('Avec ', '')))
    #print(acteur_clean)
    #Realisateur
    real = film.find("a", {"class":"blue-link"}).text
    #print(real)
    #date
    date = film.find('span', {'class':'date'}).text
    #print(date)
    #Genres
    meta_body_info = film.find("div", {"class":"meta-body-info"})
    genres = meta_body_info.find_all("span")
    del genres[0:3]
    list_genre = []
    for genre in genres:
        list_genre.append(genre.text)
    #synopsis
    synops = film.find_all("div", {"class":"content-txt"})
    synopsis=[]
    synopsis_clean=[]
    for i in synops:
        synopsis.append(i.text)
    for i in synopsis:
        synopsis_clean.append((" ".join(i.split())))
    #print(synopsis_clean)
    df = df.append({'titre':title, 'id':id_film, 'acteurs':acteur_clean, 'realisateur':real, 'date de sortie':date, 'genres':list_genre, 'synopsis':synopsis_clean}, ignore_index=True)
print(df)
    #print(list_genre)
    #print('---------------------------------------------------------------------')
