class Homebase:
    def __init__(self,longitude, latitude):
        self.Longitude = longitude
        self.Latitude = latitude

    def move_homebase(self, newLongitude, newLatitude):
        self.Longitude = newLongitude
        self.Latitude = newLatitude


