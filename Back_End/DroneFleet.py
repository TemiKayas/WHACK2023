from Drone import Drone
import math

class DroneFleet:
    def __init__(self, startLatitude, startLongitude):
        self.startLatitude = startLatitude
        self.startLongitude = startLongitude
        self.drones = []

    def add_drone(self, initial_latitude, initial_longitude, initial_altitude):
        new_drone = Drone(initial_latitude, initial_longitude, initial_altitude)
        self.drones.append(new_drone)

    def set_designated_point(self, drone_index, latitude, longitude, altitude):
        if 0 <= drone_index < len(self.drones):
            self.drones[drone_index].gps.moveTo(latitude, longitude, altitude)
        else:
            raise IndexError("Drone index out of range")

    def move_drone_to_designated_point(self, drone_index):
        if 0 <= drone_index < len(self.drones):
            drone = self.drones[drone_index]
            lat, long, alt = drone.gps.latitude, drone.gps.longitude, drone.gps.altitude
            drone.move_to(lat, long, alt)
        else:
            raise IndexError("Drone index out of range")

    def get_drone_position(self, drone_index):
        if 0 <= drone_index < len(self.drones):
            drone = self.drones[drone_index]
            return drone.gps.get_latitude(), drone.gps.get_longitude(), drone.gps.get_altitude()
        else:
            raise IndexError("Drone index out of range")
    
    def get_drone_position(self, drone_index):
        if 0 <= drone_index < len(self.drones):
            drone = self.drones[drone_index]
            return drone.gps.get_latitude(), drone.gps.get_longitude(), drone.gps.get_altitude()
        else:
            raise IndexError("Drone index out of range")

    def calculate_distance_and_bearing(self, pointALat, pointALon, pointBLat, pointBLon):
        x_distance = pointBLon - pointALon
        y_distance = pointBLat - pointALat
        distance = math.sqrt(x_distance**2 + y_distance**2)
        bearing = math.atan2(y_distance, x_distance)
        return distance, math.degrees(bearing)

    def move_in_direction(lat, lon, distance, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        new_lat = lat + distance * math.sin(angle_radians)
        new_lon = lon + distance * math.cos(angle_radians)
        return new_lat, new_lon

    def connect_two_points(self, pointALat, pointALon, pointBLat, pointBLon):
        distance, bearing = self.calculate_distance_and_bearing(pointALat, pointALon, pointBLat, pointBLon)
        current_position_lat = pointALat
        current_position_lon = pointALon

        if(sum(drone.router_radius * .9 for drone in self.drones) < distance):
            return "Fleet is incapable of connecting the two points"

        for drone in DroneFleet:
            next_position_lat, next_position_lon = self.move_in_direction(current_position_lat, current_position_lon, drone.routerRadius, bearing)
            drone.moveTo(next_position_lat, next_position_lon, drone.gps.get_altitude)
            current_position_lat, current_position_lon = next_position_lat, next_position_lon

