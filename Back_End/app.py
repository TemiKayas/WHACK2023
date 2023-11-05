from flask import Flask, request, jsonify
from DroneFleet import DroneFleet  # Replace with your actual module/file name

app = Flask(__name__)

# Assume we have a global DroneFleet instance for simplicity
# You may want to handle multiple fleets using sessions or a database
drone_fleet = DroneFleet(startLatitude=0.0, startLongitude=0.0)

@app.route('/add_drone', methods=['POST'])
def add_drone():
    data = request.json
    try:
        drone_fleet.add_drone(
            initial_latitude=data['latitude'],
            initial_longitude=data['longitude'],
            initial_altitude=data['altitude']
        )
        return jsonify({"success": True}), 200
    except KeyError:
        return jsonify({"error": "Invalid drone data"}), 400

@app.route('/remove_drone', methods=['POST'])
def remove_drone():
    data = request.json
    drone_index = data.get('index')
    if drone_index is not None and 0 <= drone_index < len(drone_fleet.drones):
        del drone_fleet.drones[drone_index]
        return jsonify({"success": True}), 200
    return jsonify({"error": "Invalid drone index"}), 400

@app.route('/connect_two_points', methods=['POST'])
def connect_two_points():
    data = request.json
    try:
        result = drone_fleet.connect_two_points(
            pointALat=data['pointA']['lat'],
            pointALon=data['pointA']['lon'],
            pointBLat=data['pointB']['lat'],
            pointBLon=data['pointB']['lon']
        )
        if result == "Fleet is incapable of connecting the two points":
            return jsonify({"error": result}), 400
        return jsonify({"success": True, "message": result}), 200
    except KeyError:
        return jsonify({"error": "Invalid point data"}), 400
 
if __name__ == '__main__':
    app.run()
