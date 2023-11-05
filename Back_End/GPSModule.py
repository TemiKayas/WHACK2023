import time
import threading
from flask import Flask
app = Flask(__name__)

class GPSModule:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.initial_latitude = latitude
        self.initial_longitude = longitude 

    def get_initial_latitude(self):
        return self.initial_latitude

    def get_initial_longitude(self):
        return self.initial_longitude

    def update_position(self, new_latitude, new_longitude, new_altitude):
        self.latitude = new_latitude
        self.longitude = new_longitude
        self.altitude = new_altitude
        print(f"New position - Latitude: {self.latitude}, Longitude: {self.longitude}, Altitude: {self.altitude} km")

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_altitude(self):
        return self.altitude

    def update_altitude(self, new_altitude):
        self.altitude = new_altitude
        print(f"Altitude updated to {self.altitude} km")

    def move_to(self, new_latitude, new_longitude, new_altitude):
        self.update_position(new_latitude, new_longitude, new_altitude)

