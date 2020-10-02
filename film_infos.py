from datetime import date
from people_infos import PeopleInfo
class FilmInfo:

    def __init__(self):
        self.id = None
        self.title = None
        self.date = None
        self.provider_id = None
        self.actors = []
        self.director = []
        self.genres = []
        self.synopsis = None
        self.notes = (None,None)

    def to_dictionary(self): #TODO: à finir!!! fonction de sérialisation
        return {
        'title':self.title,
        'id':self.provider_id, 
        'actors': ", ".join(a.full_name for a in self.actors),
        'directors': ", ".join(a.full_name for a in self.director), 
        'date':self.date, 
        'genres': ", ".join(self.genres), 
        'synopsis':self.synopsis,
        'notes_presse': self.notes[0],
        'note_spec': self.notes[1]
        }
    

    