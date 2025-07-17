import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { weatherAPI } from '../services/api';
import { format } from 'date-fns';
import './WeatherDashboard.css';

const WeatherDashboard = () => {
  const [selectedCity, setSelectedCity] = useState('New York');
  const [weatherHistory, setWeatherHistory] = useState([]);
  const [latestReadings, setLatestReadings] = useState([]);
  const [loading, setLoading] = useState(false);

  const cities = ['New York', 'London', 'Tokyo', 'Sydney', 'Mumbai', 'Berlin', 'Paris', 'Toronto', 'Singapore', 'Dubai'];

  useEffect(() => {
    fetchWeatherHistory();
    fetchLatestReadings();
    
    // Refresh data every 2 minutes
    const interval = setInterval(() => {
      fetchWeatherHistory();
      fetchLatestReadings();
    }, 120000);

    return () => clearInterval(interval);
  }, [selectedCity]);

  const fetchWeatherHistory = async () => {
    setLoading(true);
    try {
      const response = await weatherAPI.getWeatherHistory(selectedCity, 24);
      const formattedData = response.data.map(reading => ({
        ...reading,
        time: format(new Date(reading.timestamp), 'HH:mm'),
        fullTime: reading.timestamp
      })).reverse(); // Reverse to show chronological order
      
      setWeatherHistory(formattedData);
    } catch (error) {
      console.error('Error fetching weather history:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLatestReadings = async () => {
    try {
      const response = await weatherAPI.getLatestReadings(10);
      setLatestReadings(response.data);
    } catch (error) {
      console.error('Error fetching latest readings:', error);
    }
  };

  const getAQIColor = (aqi) => {
    if (aqi <= 50) return '#4CAF50';
    if (aqi <= 100) return '#FFEB3B';
    if (aqi <= 150) return '#FF9800';
    if (aqi <= 200) return '#F44336';
    return '#9C27B0';
  };

  const getAQILabel = (aqi) => {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive';
    if (aqi <= 200) return 'Unhealthy';
    return 'Very Unhealthy';
  };

  return (
    <div className="weather-dashboard">
      <div className="dashboard-header">
        <h2>Weather Dashboard</h2>
        <select 
          value={selectedCity} 
          onChange={(e) => setSelectedCity(e.target.value)}
          className="city-selector"
        >
          {cities.map(city => (
            <option key={city} value={city}>{city}</option>
          ))}
        </select>
      </div>

      {loading && <div className="loading">Loading weather data...</div>}

      {/* Current Weather Cards */}
      <div className="current-weather-grid">
        {latestReadings.slice(0, 4).map((reading, index) => (
          <div key={index} className="weather-card">
            <h3>{reading.city}</h3>
            <div className="weather-main">
              <span className="temperature">{reading.temperature.toFixed(1)}°C</span>
              <span className="condition">{reading.weather_condition}</span>
            </div>
            <div className="weather-details">
              <div>Humidity: {reading.humidity}%</div>
              <div>Pressure: {reading.pressure} hPa</div>
              {reading.aqi && (
                <div style={{ color: getAQIColor(reading.aqi) }}>
                  AQI: {reading.aqi} ({getAQILabel(reading.aqi)})
                </div>
              )}
            </div>
            <div className="timestamp">
              {format(new Date(reading.timestamp), 'MMM dd, HH:mm')}
            </div>
          </div>
        ))}
      </div>

      {/* Temperature Trend Chart */}
      <div className="chart-container">
        <h3>Temperature Trend - {selectedCity} (Last 24 Hours)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={weatherHistory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip 
              labelFormatter={(value) => `Time: ${value}`}
              formatter={(value, name) => [`${value}°C`, 'Temperature']}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="temperature" 
              stroke="#ff6b6b" 
              strokeWidth={2}
              dot={{ fill: '#ff6b6b', strokeWidth: 2, r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Humidity Chart */}
      <div className="chart-container">
        <h3>Humidity Levels - {selectedCity}</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={weatherHistory.slice(-12)}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip formatter={(value) => [`${value}%`, 'Humidity']} />
            <Bar dataKey="humidity" fill="#4ecdc4" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Multi-metric Chart */}
      <div className="chart-container">
        <h3>Weather Metrics Overview - {selectedCity}</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={weatherHistory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis yAxisId="left" />
            <YAxis yAxisId="right" orientation="right" />
            <Tooltip />
            <Legend />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="temperature" 
              stroke="#ff6b6b" 
              name="Temperature (°C)"
            />
            <Line 
              yAxisId="right"
              type="monotone" 
              dataKey="humidity" 
              stroke="#4ecdc4" 
              name="Humidity (%)"
            />
            {weatherHistory.some(d => d.aqi) && (
              <Line 
                yAxisId="right"
                type="monotone" 
                dataKey="aqi" 
                stroke="#ffa726" 
                name="AQI"
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default WeatherDashboard;