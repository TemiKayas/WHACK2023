from GPSModule import GPSModule
import threading

class Drone:
    def __init__(self, initial_latitude, initial_longitude, initial_altitude, batteryLife, maxRange, payload, payloadWeight, active, routerRadius):
        self.gps = GPSModule(initial_latitude, initial_longitude, initial_altitude)
        self.batteryLife = batteryLife
        self.maxRange = maxRange
        self.payload = payload
        self.payloadWeight = payloadWeight
        self.activity = active 
        self.routerRadius = routerRadius

    def move_to(self, new_latitude, new_longitude, new_altitude):
        self.gps.update_position(new_latitude, new_longitude, new_altitude)

    def print_current_position(self):
        print(f"Current GPS Position - Latitude: {self.gps.get_latitude()}, "
              f"Longitude: {self.gps.get_longitude()}, Altitude: {self.gps.get_altitude()} km")
    
    def battery_life(self):
        return self.batteryLife

    def max_range(self):
        return self.maxRange

    def payload(self):
        return self.payload

    def payload_weight(self):
        return self.payloadWeight

    def is_active(self):
        return self.active

    def router_radius(self):
        return self.routerRadius

    def gps_coordinates(self):
        return (self.gps.latitude, self.gps.longitude, self.gps.altitude)
