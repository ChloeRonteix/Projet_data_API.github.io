import requests
import bs4
import time
import pandas as pd

url = 'http://www.allocine.fr/films/?page='

def get_pages(url, nb):
    pages = []
    for i in range(1,nb+1):
        j = url + str(i)
        pages.append(j)
    return pages
    
pages = get_pages(url,2)

df2 = pd.DataFrame(columns=('titre', 'id', 'acteurs', 'realisateur', 'date de sortie', 'genres', 'synopsis'))
for i in pages:

    response = requests.get(i)
    print(response)
         
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    em_box = soup.find_all("div", {"class":"entity-card-list"})
    print(len(em_box))
    print(em_box[-1].find("a", {"class":"meta-title-link"}).text)
        
        
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
        acteur_clean = []
        try:
            actors = film.find('div', {'class':'meta-body-actor'})
            acteur_clean.append((" ".join(actors.text.split()).replace('Avec ', '')))
        except:
            acteur_clean.append("non communiqué")
            print(f"pas d'acteurs pour le film {title}")
        #print(acteur_clean)
        #Realisateur
        real = film.find("a", {"class":"blue-link"}).text
        #print(real)
        #date
        try:
            date = film.find('span', {'class':'date'}).text
        except:
            date = "non communiquée"
            print(f'pas de date pour le film {title}')
        #print(date)
        #Genres
        meta_body_info = film.find("div", {"class":"meta-body-info"})
        genres = meta_body_info.find_all("span")
        del genres[0:3]
        list_genre = []
        for genre in genres:
            list_genre.append(genre.text)
        #synopsis
        synopsis=[]
        synopsis_clean=[]
        try:
            synops = film.find_all("div", {"class":"content-txt"})
            for i in synops:
                synopsis.append(i.text)
            for i in synopsis:
                synopsis_clean.append((" ".join(i.split())))
        except:
            synopsis_clean.append("non communiqué")
            print(f'pas de synopsis pour le film {title}')
        #print(synopsis_clean)
        df2 = df2.append({'titre':title, 'id':id_film, 'acteurs':acteur_clean, 'realisateur':real, 'date de sortie':date, 'genres':list_genre, 'synopsis':synopsis_clean}, ignore_index=True)
        time.sleep(5)
        

df2['Genres'] = [', '.join(map(str, l)) for l in df2['genres']]
df2['Synopsis'] = [', '.join(map(str, l)) for l in df2['synopsis']]
df2['Acteurs'] = [', '.join(map(str, l)) for l in df2['acteurs']]
data = df2.drop(columns=['acteurs','synopsis','genres'])

print("FINI")

print(data)