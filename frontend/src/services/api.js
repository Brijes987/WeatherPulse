import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const weatherAPI = {
  getCurrentWeather: (city) => 
    api.get(`/api/weather/current/${city}`),
  
  getWeatherHistory: (city, hours = 24) => 
    api.get(`/api/weather/history/${city}?hours=${hours}`),
  
  getLatestReadings: (limit = 10) => 
    api.get(`/api/weather/latest?limit=${limit}`),
};

export const alertsAPI = {
  getAlerts: (params = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    return api.get(`/api/alerts?${queryParams}`);
  },
  
  resolveAlert: (alertId) => 
    api.put(`/api/alerts/${alertId}/resolve`),
  
  getAlertStats: (hours = 24) => 
    api.get(`/api/alerts/stats?hours=${hours}`),
};

export default api;