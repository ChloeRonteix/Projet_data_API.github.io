insert_film = '''
INSERT INTO films (provider_id, title, date, synopsis, note_press, note_people) 
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING id;
'''

save_scraped_page = '''
TRUNCATE scrap_progress;
INSERT INTO scrap_progress (page_id) VALUES (%s);
'''
get_last_scraped_page = "SELECT page_id FROM scrap_progress;"

insert_genre = '''
INSERT INTO genres (name)
VALUES (%s)
RETURNING id;
'''

get_genre_id_by_name = '''
SELECT id 
FROM genres
WHERE name = %s;
'''

insert_genre_for_film = '''
INSERT INTO films_genres (id_film, id_genre)
VALUES (%s, %s);
'''

get_film_id_by_provider_id = '''
SELECT id FROM films
WHERE provider_id = %s;
'''

insert_people = '''
INSERT INTO people (full_name, provider_id)
VALUES (%s, %s)
RETURNING id;
'''

insert_actor_for_film = '''
INSERT INTO films_actors (id_film, id_actor)
VALUES (%s, %s);
'''

insert_director_for_film = '''
INSERT INTO films_directors (id_film, id_director)
VALUES (%s, %s);
'''

get_people_id_by_name_and_provider_id = '''
SELECT id 
FROM people
WHERE full_name = %s
AND COALESCE(provider_id,0) = COALESCE(%s,0);
'''

get_film_by_id = '''
SELECT id, provider_id, title, date, synopsis, note_press, note_people 
FROM films WHERE id = %s
'''

get_genres_film = '''
SELECT g.name FROM genres g 
JOIN films_genres fg ON g.id = fg.id_genre 
WHERE fg.id_film = %s;
'''

get_actors_by_film = '''
SELECT p.full_name FROM people p 
JOIN films_actors fa ON p.id = fa.id_actor 
WHERE fa.id_film = %s
'''

get_directors_by_film = '''
SELECT p.full_name FROM people p 
JOIN films_directors fa ON p.id = fa.id_director 
WHERE fa.id_film = %s
'''

get_people_by_id = '''
SELECT id, provider_id, full_name FROM people WHERE id = %s
'''

get_films_by_actor = '''
SELECT f.title, extract( year from f.date)::int FROM films f 
JOIN films_actors fa ON f.id = fa.id_film 
WHERE fa.id_actor = %s;
'''

get_films_by_director = '''
SELECT f.title, extract( year from f.date)::int FROM films f 
JOIN films_directors fa ON f.id = fa.id_film 
WHERE fa.id_director = %s;
'''

get_all_genres = '''
SELECT name FROM genres;
'''

get_genre_by_id = '''
SELECT name FROM genres
WHERE id = %s;
'''

get_films_by_genre = '''
SELECT f.title from films f
JOIN films_genres fg ON f.id = fg.id_film
JOIN genres g ON g.id = fg.id_genre
WHERE g.name = %s;
'''

count_films_by_month = '''
SELECT extract(month from date)::int, count(*) from films
group by extract(month from date)
ORDER by extract(month from date);
'''

count_films_by_genre = '''
SELECT g.name, count(f.*) from films f
JOIN films_genres fg on fg.id_film = f.id
JOIN genres g on g.id = fg.id_genre
GROUP BY g.name;
'''