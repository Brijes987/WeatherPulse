import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import WeatherDashboard from './components/WeatherDashboard';
import AlertPanel from './components/AlertPanel';
import MapSelector from './components/MapSelector';
import Login from './components/Login';
import Register from './components/Register';
import { useWebSocket } from './hooks/useWebSocket';
import { weatherAPI } from './services/api';
import './App.css';

function App() {
  const [alerts, setAlerts] = useState([]);
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(true);
  const [userCities, setUserCities] = useState([]);
  const [latestWeatherData, setLatestWeatherData] = useState([]);
  
  // WebSocket connection for real-time alerts
  const { lastMessage, connectionStatus } = useWebSocket(
    user ? 'ws://localhost:8000/ws' : null
  );
  
  useEffect(() => {
    // Check for existing token
    const token = localStorage.getItem('token');
    if (token) {
      fetchUserProfile(token);
    }
  }, []);

  useEffect(() => {
    if (user) {
      fetchUserCities();
      fetchLatestWeatherData();
    }
  }, [user]);
  
  useEffect(() => {
    if (lastMessage) {
      const alertData = JSON.parse(lastMessage.data);
      
      // Add to alerts list
      setAlerts(prev => [alertData, ...prev.slice(0, 49)]); // Keep last 50 alerts
      
      // Show toast notification
      toast.warn(alertData.message, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });
    }
  }, [lastMessage]);

  const fetchUserProfile = async (token) => {
    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        localStorage.removeItem('token');
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      localStorage.removeItem('token');
    }
  };

  const fetchUserCities = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/user/cities', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const cities = await response.json();
        setUserCities(cities);
      }
    } catch (error) {
      console.error('Error fetching user cities:', error);
    }
  };

  const fetchLatestWeatherData = async () => {
    try {
      const response = await weatherAPI.getLatestReadings(20);
      setLatestWeatherData(response.data);
    } catch (error) {
      console.error('Error fetching latest weather data:', error);
    }
  };

  const handleLogin = (token) => {
    fetchUserProfile(token);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setUserCities([]);
    setAlerts([]);
  };

  const handleLocationSelect = (location) => {
    console.log('Selected location:', location);
    // You can add logic here to fetch weather for the selected location
  };

  const handleCityAdd = async (cityData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/user/cities', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(cityData)
      });
      
      if (response.ok) {
        toast.success('City added successfully!');
        fetchUserCities(); // Refresh the list
      } else {
        toast.error('Failed to add city');
      }
    } catch (error) {
      console.error('Error adding city:', error);
      toast.error('Error adding city');
    }
  };

  // Show authentication if user is not logged in
  if (!user) {
    return (
      <>
        {showLogin ? (
          <Login 
            onLogin={handleLogin}
            onSwitchToRegister={() => setShowLogin(false)}
          />
        ) : (
          <Register 
            onSwitchToLogin={() => setShowLogin(true)}
          />
        )}
        <ToastContainer />
      </>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-left">
          <h1>🌤️ Weather Monitoring System</h1>
          <div className="connection-status">
            Status: <span className={connectionStatus === 'Connected' ? 'connected' : 'disconnected'}>
              {connectionStatus}
            </span>
          </div>
        </div>
        <div className="header-right">
          <span className="user-welcome">Welcome, {user.username}!</span>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>
      
      <main className="App-main">
        <div className="dashboard-layout">
          {/* Map Section */}
          <div className="map-section">
            <MapSelector 
              weatherData={latestWeatherData}
              onLocationSelect={handleLocationSelect}
              userCities={userCities}
              onCityAdd={handleCityAdd}
            />
          </div>
          
          {/* Dashboard Section */}
          <div className="dashboard-container">
            <WeatherDashboard />
            <AlertPanel alerts={alerts} />
          </div>
        </div>
      </main>
      
      <ToastContainer />
    </div>
  );
}

export default App;