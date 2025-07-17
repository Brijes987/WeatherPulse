import React, { useState, useEffect } from 'react';
import { alertsAPI } from '../services/api';
import { format } from 'date-fns';
import './AlertPanel.css';

const AlertPanel = ({ alerts: realtimeAlerts }) => {
  const [historicalAlerts, setHistoricalAlerts] = useState([]);
  const [alertStats, setAlertStats] = useState(null);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistoricalAlerts();
    fetchAlertStats();
    
    // Refresh every 5 minutes
    const interval = setInterval(() => {
      fetchHistoricalAlerts();
      fetchAlertStats();
    }, 300000);

    return () => clearInterval(interval);
  }, [filter]);

  const fetchHistoricalAlerts = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filter !== 'all') {
        params.alert_type = filter;
      }
      params.hours = 24;
      params.limit = 20;

      const response = await alertsAPI.getAlerts(params);
      setHistoricalAlerts(response.data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAlertStats = async () => {
    try {
      const response = await alertsAPI.getAlertStats(24);
      setAlertStats(response.data);
    } catch (error) {
      console.error('Error fetching alert stats:', error);
    }
  };

  const handleResolveAlert = async (alertId) => {
    try {
      await alertsAPI.resolveAlert(alertId);
      fetchHistoricalAlerts(); // Refresh the list
    } catch (error) {
      console.error('Error resolving alert:', error);
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'temperature': return '🌡️';
      case 'humidity': return '💧';
      case 'aqi': return '🏭';
      default: return '⚠️';
    }
  };

  const getAlertColor = (type) => {
    switch (type) {
      case 'temperature': return '#ff6b6b';
      case 'humidity': return '#4ecdc4';
      case 'aqi': return '#ffa726';
      default: return '#666';
    }
  };

  // Combine realtime and historical alerts, removing duplicates
  const allAlerts = [
    ...realtimeAlerts,
    ...historicalAlerts.filter(ha => 
      !realtimeAlerts.some(ra => ra.id === ha.id)
    )
  ].sort((a, b) => new Date(b.created_at || b.timestamp) - new Date(a.created_at || a.timestamp));

  return (
    <div className="alert-panel">
      <div className="alert-header">
        <h2>🚨 Alert Center</h2>
        <select 
          value={filter} 
          onChange={(e) => setFilter(e.target.value)}
          className="alert-filter"
        >
          <option value="all">All Alerts</option>
          <option value="temperature">Temperature</option>
          <option value="humidity">Humidity</option>
          <option value="aqi">Air Quality</option>
        </select>
      </div>

      {/* Alert Statistics */}
      {alertStats && (
        <div className="alert-stats">
          <div className="stat-card">
            <div className="stat-number">{alertStats.total_alerts}</div>
            <div className="stat-label">Total (24h)</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{alertStats.unresolved_alerts}</div>
            <div className="stat-label">Unresolved</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{alertStats.resolved_alerts}</div>
            <div className="stat-label">Resolved</div>
          </div>
        </div>
      )}

      {/* Alert Type Breakdown */}
      {alertStats && (
        <div className="alert-breakdown">
          <h4>Alert Types (24h)</h4>
          <div className="breakdown-items">
            <div className="breakdown-item">
              <span className="breakdown-icon">🌡️</span>
              <span className="breakdown-label">Temperature</span>
              <span className="breakdown-count">{alertStats.by_type.temperature}</span>
            </div>
            <div className="breakdown-item">
              <span className="breakdown-icon">💧</span>
              <span className="breakdown-label">Humidity</span>
              <span className="breakdown-count">{alertStats.by_type.humidity}</span>
            </div>
            <div className="breakdown-item">
              <span className="breakdown-icon">🏭</span>
              <span className="breakdown-label">Air Quality</span>
              <span className="breakdown-count">{alertStats.by_type.aqi}</span>
            </div>
          </div>
        </div>
      )}

      {/* Alert List */}
      <div className="alert-list">
        <h3>Recent Alerts</h3>
        {loading && <div className="loading">Loading alerts...</div>}
        
        {allAlerts.length === 0 && !loading && (
          <div className="no-alerts">
            <div className="no-alerts-icon">✅</div>
            <div>No alerts in the last 24 hours</div>
            <div className="no-alerts-subtitle">All systems normal</div>
          </div>
        )}

        {allAlerts.map((alert, index) => (
          <div 
            key={alert.id || index} 
            className={`alert-item ${alert.is_resolved ? 'resolved' : 'active'}`}
          >
            <div className="alert-content">
              <div className="alert-header-item">
                <span 
                  className="alert-icon"
                  style={{ color: getAlertColor(alert.alert_type || alert.type) }}
                >
                  {getAlertIcon(alert.alert_type || alert.type)}
                </span>
                <span className="alert-city">{alert.city}</span>
                <span className="alert-time">
                  {format(new Date(alert.created_at || alert.timestamp), 'MMM dd, HH:mm')}
                </span>
              </div>
              <div className="alert-message">{alert.message}</div>
              {alert.threshold_value && (
                <div className="alert-details">
                  Threshold: {alert.threshold_value} | Actual: {alert.actual_value}
                </div>
              )}
            </div>
            
            {!alert.is_resolved && alert.id && (
              <button 
                className="resolve-btn"
                onClick={() => handleResolveAlert(alert.id)}
                title="Mark as resolved"
              >
                ✓
              </button>
            )}
            
            {alert.is_resolved && (
              <div className="resolved-badge">Resolved</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertPanel;