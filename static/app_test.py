import flask
from flask import request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn_string = "host='allocine.cnlsqrwefkra.eu-west-1.rds.amazonaws.com'" "dbname='postgres'" "user='common'" "password='allocine'" 
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM films LIMIT 50')
    all_movies = cursor.fetchall()
    json_movies = jsonify(all_movies)
    return json_movies

app.run()