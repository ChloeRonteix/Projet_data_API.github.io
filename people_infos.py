import json

class PeopleInfo:

    def __init__(self, full_name:str, provider_id:int):
        self.full_name = full_name
        self.provider_id = provider_id
        self.id = None
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)
    

    