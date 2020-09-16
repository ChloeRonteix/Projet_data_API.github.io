from datetime import date
from actor_infos import ActorInfo
class FilmInfo:

    def __init__(self):
        self.title = str
        self.date = date
        self.id = int
        self.actors = []
        self.director = []
        self.genre = []
        self.synopsis = str
        self.notes = (float,float)

    def to_dictionary(self): #TODO: à finir!!! fonction de sérialisation
        return {
        'title':self.title,
        'id':self.id, 
        'actors': ", ".join(a.full_name for a in self.actors),
        'directors': ", ".join(self.director), 
        'date':self.date, 
        'genres': ", ".join(self.genre), 
        'synopsis':self.synopsis,
        'notes_presse': self.notes[0],
        'note_spec': self.notes[1]
        }

    