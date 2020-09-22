from datetime import date
from people_infos import PeopleInfo
import json
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
    
    def toJSON(self):
        return json.dumps(self, default=self.default_json, sort_keys=True)

    def default_json(self, value):
        if isinstance(value, date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    