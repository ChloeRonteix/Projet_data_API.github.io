DROP TABLE IF EXISTS films;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS films_genres;
DROP TABLE IF EXISTS films_actors;

CREATE TABLE IF NOT EXISTS films (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER,
    title VARCHAR(150),
    date DATE,
    synopsis TEXT,
    note_press REAL,
    note_people REAL
);

CREATE TABLE IF NOT EXISTS directors (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER,
    full_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS actors (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER,
    full_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS films_genres (
    id SERIAL PRIMARY KEY,
    id_film INTEGER,
    id_genre INTEGER,
    FOREIGN KEY (id_film) REFERENCES films(id),
    FOREIGN KEY (id_genre) REFERENCES genres(id)
);

CREATE TABLE IF NOT EXISTS films_actors (
    id SERIAL PRIMARY KEY,
    id_film INTEGER,
    id_actor INTEGER,
    FOREIGN KEY (id_film) REFERENCES films(id),
    FOREIGN KEY (id_actor) REFERENCES actors(id)
);

CREATE TABLE IF NOT EXISTS films_directors (
    id SERIAL PRIMARY KEY,
    id_film INTEGER,
    id_director INTEGER,
    FOREIGN KEY (id_film) REFERENCES films(id),
    FOREIGN KEY (id_director) REFERENCES directors(id)
);