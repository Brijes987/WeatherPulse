import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './MapSelector.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom weather marker icons
const createWeatherIcon = (temperature, condition) => {
  const getWeatherEmoji = (condition) => {
    const conditionMap = {
      'Clear': '☀️',
      'Clouds': '☁️',
      'Rain': '🌧️',
      'Snow': '❄️',
      'Thunderstorm': '⛈️',
      'Drizzle': '🌦️',
      'Mist': '🌫️',
      'Fog': '🌫️'
    };
    return conditionMap[condition] || '🌤️';
  };

  const emoji = getWeatherEmoji(condition);
  
  return L.divIcon({
    html: `
      <div class="weather-marker">
        <div class="weather-emoji">${emoji}</div>
        <div class="weather-temp">${Math.round(temperature)}°</div>
      </div>
    `,
    className: 'custom-weather-marker',
    iconSize: [60, 60],
    iconAnchor: [30, 60]
  });
};

const LocationMarker = ({ onLocationSelect }) => {
  const [position, setPosition] = useState(null);

  useMapEvents({
    click(e) {
      setPosition(e.latlng);
      onLocationSelect(e.latlng);
    },
  });

  return position === null ? null : (
    <Marker position={position}>
      <Popup>
        Selected Location: <br />
        Lat: {position.lat.toFixed(4)} <br />
        Lng: {position.lng.toFixed(4)}
      </Popup>
    </Marker>
  );
};

const MapSelector = ({ weatherData, onLocationSelect, userCities, onCityAdd }) => {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [locationName, setLocationName] = useState('');
  const [isAddingCity, setIsAddingCity] = useState(false);

  const handleLocationSelect = async (latlng) => {
    setSelectedLocation(latlng);
    
    // Reverse geocoding to get city name
    try {
      const response = await fetch(
        `https://api.openweathermap.org/geo/1.0/reverse?lat=${latlng.lat}&lon=${latlng.lng}&limit=1&appid=${process.env.REACT_APP_OPENWEATHER_API_KEY}`
      );
      const data = await response.json();
      
      if (data.length > 0) {
        const cityName = data[0].name;
        setLocationName(cityName);
        onLocationSelect({ ...latlng, city: cityName });
      }
    } catch (error) {
      console.error('Error getting location name:', error);
    }
  };

  const handleAddCity = async () => {
    if (selectedLocation && locationName) {
      try {
        await onCityAdd({
          city: locationName,
          latitude: selectedLocation.lat,
          longitude: selectedLocation.lng,
          is_favorite: false
        });
        setIsAddingCity(false);
        setSelectedLocation(null);
        setLocationName('');
      } catch (error) {
        console.error('Error adding city:', error);
      }
    }
  };

  return (
    <div className="map-selector">
      <div className="map-header">
        <h3>🗺️ Interactive Weather Map</h3>
        <div className="map-controls">
          <button 
            className={`map-btn ${isAddingCity ? 'active' : ''}`}
            onClick={() => setIsAddingCity(!isAddingCity)}
          >
            {isAddingCity ? 'Cancel' : 'Add Location'}
          </button>
        </div>
      </div>

      <div className="map-container-wrapper">
        <MapContainer
          center={[40.7128, -74.0060]} // New York
          zoom={3}
          style={{ height: '400px', width: '100%' }}
          className="weather-map"
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {/* Weather markers for current data */}
          {weatherData.map((weather, index) => {
            // You'll need to add lat/lng to your weather data or use a geocoding service
            const coordinates = getCityCoordinates(weather.city);
            if (!coordinates) return null;
            
            return (
              <Marker
                key={index}
                position={[coordinates.lat, coordinates.lng]}
                icon={createWeatherIcon(weather.temperature, weather.weather_condition)}
              >
                <Popup>
                  <div className="weather-popup">
                    <h4>{weather.city}</h4>
                    <div className="popup-weather">
                      <div className="popup-temp">{weather.temperature.toFixed(1)}°C</div>
                      <div className="popup-condition">{weather.weather_condition}</div>
                    </div>
                    <div className="popup-details">
                      <div>Humidity: {weather.humidity}%</div>
                      <div>Pressure: {weather.pressure} hPa</div>
                      {weather.aqi && <div>AQI: {weather.aqi}</div>}
                    </div>
                    <div className="popup-time">
                      {new Date(weather.timestamp).toLocaleString()}
                    </div>
                  </div>
                </Popup>
              </Marker>
            );
          })}

          {/* User's saved cities */}
          {userCities.map((city, index) => (
            <Marker
              key={`user-${index}`}
              position={[city.latitude, city.longitude]}
              icon={L.divIcon({
                html: `<div class="user-city-marker">${city.is_favorite ? '⭐' : '📍'}</div>`,
                className: 'custom-user-marker',
                iconSize: [30, 30],
                iconAnchor: [15, 30]
              })}
            >
              <Popup>
                <div className="user-city-popup">
                  <h4>{city.city} {city.is_favorite && '⭐'}</h4>
                  <p>Your saved location</p>
                </div>
              </Popup>
            </Marker>
          ))}

          {/* Location selector when adding cities */}
          {isAddingCity && <LocationMarker onLocationSelect={handleLocationSelect} />}
        </MapContainer>
      </div>

      {/* Add city form */}
      {isAddingCity && selectedLocation && (
        <div className="add-city-form">
          <div className="form-group">
            <label>Location: {locationName || 'Loading...'}</label>
            <div className="coordinates">
              Lat: {selectedLocation.lat.toFixed(4)}, Lng: {selectedLocation.lng.toFixed(4)}
            </div>
          </div>
          <div className="form-actions">
            <button className="btn-primary" onClick={handleAddCity} disabled={!locationName}>
              Add to My Cities
            </button>
            <button className="btn-secondary" onClick={() => setIsAddingCity(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="map-legend">
        <h4>Legend</h4>
        <div className="legend-items">
          <div className="legend-item">
            <span className="legend-icon weather-icon">🌤️</span>
            <span>Weather Stations</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon">📍</span>
            <span>Your Cities</span>
          </div>
          <div className="legend-item">
            <span className="legend-icon">⭐</span>
            <span>Favorites</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper function to get coordinates for major cities
const getCityCoordinates = (cityName) => {
  const coordinates = {
    'New York': { lat: 40.7128, lng: -74.0060 },
    'London': { lat: 51.5074, lng: -0.1278 },
    'Tokyo': { lat: 35.6762, lng: 139.6503 },
    'Sydney': { lat: -33.8688, lng: 151.2093 },
    'Mumbai': { lat: 19.0760, lng: 72.8777 },
    'Berlin': { lat: 52.5200, lng: 13.4050 },
    'Paris': { lat: 48.8566, lng: 2.3522 },
    'Toronto': { lat: 43.6532, lng: -79.3832 },
    'Singapore': { lat: 1.3521, lng: 103.8198 },
    'Dubai': { lat: 25.2048, lng: 55.2708 }
  };
  
  return coordinates[cityName];
};

export default MapSelector;