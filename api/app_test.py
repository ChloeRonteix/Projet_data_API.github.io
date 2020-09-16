import flask 
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# test dict

# visit http://127.0.0.1:5000/api/v1/resources/books/all

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'name': 'zizi'},
    {'id': 1,
     'name': 'pipi',},
    {'id': 2,
     'title': 'La divine Comedie'} # /! UTF8 "é" non supporté
    ]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

app.run()