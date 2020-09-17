DROP TABLE IF EXISTS scrap_progress;
DROP TABLE IF EXISTS films_genres;
DROP TABLE IF EXISTS films_actors;
DROP TABLE IF EXISTS films_directors;
DROP TABLE IF EXISTS films;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS genres;

CREATE TABLE IF NOT EXISTS films (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER UNIQUE NOT NULL,
    title VARCHAR(150) NOT NULL,
    date DATE,
    synopsis TEXT,
    note_press REAL,
    note_people REAL
);

CREATE TABLE IF NOT EXISTS people (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER,
    full_name VARCHAR(50) NOT NULL,
    UNIQUE (provider_id, full_name)
);

CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS films_genres (
    id_film INTEGER NOT NULL,
    id_genre INTEGER NOT NULL,
    PRIMARY KEY (id_film, id_genre),
    FOREIGN KEY (id_film) REFERENCES films(id),
    FOREIGN KEY (id_genre) REFERENCES genres(id)
    
);

CREATE TABLE IF NOT EXISTS films_actors (
    id_film INTEGER NOT NULL,
    id_actor INTEGER NOT NULL,
    PRIMARY KEY (id_film, id_actor),
    FOREIGN KEY (id_film) REFERENCES films(id),
    FOREIGN KEY (id_actor) REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS films_directors (
    id_film INTEGER NOT NULL,
    id_director INTEGER NOT NULL,
    PRIMARY KEY (id_film, id_director),
    FOREIGN KEY (id_film) REFERENCES films(id),
    FOREIGN KEY (id_director) REFERENCES people(id)
);

CREATE TABLE IF NOT EXISTS scrap_progress (
	page_id INTEGER NOT NULL
);