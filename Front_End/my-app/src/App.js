import React, { useState } from 'react';
import './App.css';
import {
  MapContainer, TileLayer, Marker, Popup, Tooltip, Circle, useMapEvents
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import droneIconUrl from './droneicon.png';
import homeBaseIconUrl from './homebase.png';

const droneIcon = L.icon({
  iconUrl: droneIconUrl,
  iconSize: [38, 38],
  iconAnchor: [19, 38],
  popupAnchor: [0, -38]
});

const homeBaseIcon = L.icon({
  iconUrl: homeBaseIconUrl,
  iconSize: [50, 50],
  iconAnchor: [25, 50],
  popupAnchor: [0, -50]
});

const interpolatePoints = (latlng1, latlng2, radius) => {
  const distance = L.latLng(latlng1).distanceTo(latlng2);
  const numberOfCircles = Math.ceil(distance / (radius * 2));
  let points = [];
  for (let i = 1; i <= numberOfCircles; i++) {
    const weight = (i * radius * 2 - radius) / distance;
    const lat = latlng1.lat * (1 - weight) + latlng2.lat * weight;
    const lng = latlng1.lng * (1 - weight) + latlng2.lng * weight;
    points.push(L.latLng(lat, lng));
  }
  return points;
};

function LocationPopup({ onDeploy, onSetHomeBase }) {
  const [popupInfo, setPopupInfo] = useState(null);
  useMapEvents({
    click(e) {
      setPopupInfo({ latlng: e.latlng });
    },
  });

  const handleDeployClick = () => {
    if (popupInfo) {
      onDeploy(popupInfo.latlng);
      setPopupInfo(null);
    }
  };

  const handleSetHomeBaseClick = () => {
    if (popupInfo) {
      onSetHomeBase(popupInfo.latlng);
      setPopupInfo(null);
    }
  };

  return popupInfo ? (
    <Popup position={popupInfo.latlng} onClose={() => setPopupInfo(null)}>
      <div>
        <strong>Coordinates:</strong><br />
        Latitude: {popupInfo.latlng.lat.toFixed(6)}<br />
        Longitude: {popupInfo.latlng.lng.toFixed(6)}<br />
        <button onClick={handleDeployClick}>Deploy Drone Here</button>
        <button onClick={handleSetHomeBaseClick}>Set as Home Base</button>
      </div>
    </Popup>
  ) : null;
}

function DroneInfoPanel({ drones, homeBase, onRemoveDrone }) {
  const calculateDistance = (drone) => {
    return homeBase.distanceTo(drone.position).toFixed(2);
  };

  const calculateBatteryLife = (distance) => {
    // Placeholder function for battery life calculation
    return (100 - distance / 1000).toFixed(2); // Dummy calculation
  };

  const calculateETA = (distance) => {
    const speedMph = 50;
    const speedKmPerHour = speedMph * 1.60934;
    const timeHours = distance / 1000 / speedKmPerHour;
    const timeMinutes = timeHours * 60;
    return timeMinutes.toFixed(2) + 5;
  };

  const calculateSignalStrength = (distance) => {
    // Placeholder function for signal strength calculation
    return (100 - distance / 100).toFixed(2); // Dummy calculation
  };

  return (
    <div className="info-panel">
      <h1>PIGEON</h1>
      <h2>Drone Information</h2>
      <div className="home-base-info">
        <h3>Home Base Coordinates</h3>
        <p>Latitude: {homeBase.lat.toFixed(6)}</p>
        <p>Longitude: {homeBase.lng.toFixed(6)}</p>
      </div>
      {drones.map((drone, index) => {
        const distance = calculateDistance(drone);
        const batteryLife = calculateBatteryLife(distance);
        const eta = calculateETA(distance);
        const signalStrength = calculateSignalStrength(distance);

        return (
          <div key={index} className="drone-info">
            <h3>Drone Line {index + 1}</h3>
            <p>Distance from Base: {(distance / 1000).toFixed(2)} Km</p>
            <p>Battery Life: {batteryLife} %</p>
            <p>ETA at 50 MPH: {Math.floor(eta) + 3} minutes</p>
            <p>Signal Strength: {signalStrength} %</p>
            <p>Amount of Drones: {Math.floor(distance/(200) + 1)} </p>
            <button onClick={() => onRemoveDrone(index)}>Remove Drone</button>
          </div>
        );
      })}
    </div>
  );
}

function App() {
  const [drones, setDrones] = useState([]);
  const [homeBasePosition, setHomeBasePosition] = useState(L.latLng(31.418189, 34.345129));
  const [mapKey, setMapKey] = useState(Date.now()); // State to control the key of MapContainer
  const radius = 100; // radius in meters

  const handleDeployDrone = (latlng) => {
    setDrones((prevDrones) => [...prevDrones, { position: L.latLng(latlng) }]);
    setMapKey(Date.now()); // Reset the key to force MapContainer to re-render
  };

  const handleSetHomeBase = (latlng) => {
    setHomeBasePosition(L.latLng(latlng));
    setMapKey(Date.now()); // Reset the key to force MapContainer to re-render
  };

  const removeDrone = (index) => {
    setDrones((prevDrones) => prevDrones.filter((_, i) => i !== index));
    setMapKey(Date.now()); // Optionally reset the key here if you want to force a re-render
  };

  return (
    <div className="App">
      {/* Use the mapKey state as a key for MapContainer to control re-render */}
      <MapContainer key={mapKey} center={homeBasePosition} zoom={13} style={{ height: '100vh', width: '75vw', float: 'left' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={homeBasePosition} icon={homeBaseIcon}>
          <Popup>Home Base</Popup>
        </Marker>
        {drones.map((drone, index) => {
          const points = interpolatePoints(homeBasePosition, drone.position, radius);
          return (
            <React.Fragment key={index}>
              <Marker position={drone.position} icon={droneIcon}>
                <Tooltip direction="top" offset={[0, -20]} opacity={1} permanent>
                  Drone Line {index + 1}
                </Tooltip>
              </Marker>
              {points.map((point, idx) => (
                <Circle key={idx} center={point} radius={radius} color="blue" />
              ))}
            </React.Fragment>
          );
        })}
        <LocationPopup onDeploy={handleDeployDrone} onSetHomeBase={handleSetHomeBase} />
      </MapContainer>
      <DroneInfoPanel drones={drones} homeBase={homeBasePosition} onRemoveDrone={removeDrone} />
    </div>
  );
}

export default App;
