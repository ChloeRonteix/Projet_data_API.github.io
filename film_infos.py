from datetime import date
class FilmInfo:

    def __init__(self):
        self.title = str
        self.date = date
        self.id = int
        self.actors = list
        self.director = list
        self.genre = list
        self.synopsis = str
        self.notes = (float,float)

    def to_dictionary(self): #TODO: à finir!!! fonction de sérialisation
        return {
        'title':self.title,
        'id':self.id, 
        'acteurs':self.actors,
         'directors':real, 
         'date de sortie':date, 
         'genres':list_genre, 
         'synopsis':synopsis_clean
         }

    