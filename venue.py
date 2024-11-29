class Venue:
    def __init__(self, id, name, cityId):
        self.id = id
        self.name = name
        self.cityId = cityId

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cityId': self.cityId
        }
    
