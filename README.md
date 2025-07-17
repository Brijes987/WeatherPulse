# Real-Time Weather Monitoring and Alerting System

<!-- Topic Tags -->
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.2-blue?logo=react&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-orange?logo=grafana&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-green)
![JWT](https://img.shields.io/badge/JWT-Authentication-purple)
![Leaflet](https://img.shields.io/badge/Leaflet-Maps-green?logo=leaflet&logoColor=white)

**Topics:** `real-time-monitoring` `weather-api` `fastapi` `react` `websockets` `prometheus` `grafana` `docker` `postgresql` `redis` `jwt-auth` `interactive-maps` `email-notifications` `sms-alerts` `microservices`

---

A comprehensive enterprise-grade real-time weather monitoring system with user authentication, interactive maps, multi-channel notifications, and advanced monitoring capabilities.

## 🏗️ Enhanced System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                               │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   React SPA     │  Interactive    │    User Authentication      │
│  + Dashboard    │     Maps        │      + JWT Auth             │
│  + Charts       │  (Leaflet.js)   │   + Personal Settings       │
└─────────────────┴─────────────────┴─────────────────────────────┘
         ▲                       ▲                    ▲
         │ WebSocket              │ REST API           │ Auth
         │ Real-time              │                    │
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                                │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   FastAPI       │   WebSocket     │    Prometheus Metrics       │
│  + JWT Auth     │   Manager       │    + System Monitoring      │
│  + REST APIs    │  + Real-time    │    + Performance Tracking   │
└─────────────────┴─────────────────┴─────────────────────────────┘
         ▲                       ▲                    ▲
         │                       │                    │
┌─────────────────────────────────────────────────────────────────┐
│                   DATA & MESSAGING LAYER                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   PostgreSQL    │     Redis       │    Notification Services    │
│  + User Data    │  + Pub/Sub      │    + Email (SMTP)           │
│  + Weather Data │  + Caching      │    + SMS (Twilio)           │
│  + Alerts       │  + Sessions     │    + Real-time Alerts       │
└─────────────────┴─────────────────┴─────────────────────────────┘
         ▲                       ▲                    ▲
         │                       │                    │
┌─────────────────────────────────────────────────────────────────┐
│                 MONITORING & SCHEDULING LAYER                  │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  Weather Cron   │   Prometheus    │       Grafana               │
│  Scheduler      │   + Metrics     │    + Dashboards             │
│  + Auto Fetch   │   + Alerting    │    + Visualization          │
│  + Threshold    │   + Rules       │    + System Health          │
│    Detection    │                 │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
         ▲
         │
┌─────────────────┐
│ OpenWeatherMap  │
│      API        │
│  + Weather Data │
│  + Air Quality  │
└─────────────────┘
```

## 🚀 Core Features

### 🔐 **User Authentication & Management**
- **JWT-based Authentication**: Secure login/signup system
- **Personal Dashboards**: Customized user experience
- **Custom Alert Thresholds**: User-defined temperature, humidity, and AQI limits
- **City Management**: Add/remove favorite cities with interactive map

### 📤 **Multi-Channel Notifications**
- **Real-time WebSocket Alerts**: Instant browser notifications
- **Email Notifications**: HTML-formatted alerts via SMTP
- **SMS Alerts**: Text message notifications via Twilio
- **Bulk Notifications**: Concurrent delivery for performance
- **User Preferences**: Toggle email/SMS per alert type

### 🌍 **Interactive Geo-Mapping**
- **Leaflet.js Integration**: Interactive world map interface
- **Weather Visualization**: Real-time weather markers with conditions
- **Click-to-Add Locations**: Select any global location for monitoring
- **User City Markers**: Visual indicators for saved locations
- **Reverse Geocoding**: Automatic city name resolution

### 📈 **Advanced Monitoring & Analytics**
- **Prometheus Metrics**: System performance and API monitoring
- **Grafana Dashboards**: Real-time visualization and alerting
- **System Health Tracking**: CPU, memory, disk usage monitoring
- **API Performance Metrics**: Request rates, response times, error tracking
- **Weather Data Analytics**: Fetch success rates, alert statistics

### 📊 **Data Visualization & Insights**
- **Interactive Charts**: Temperature trends, humidity levels, AQI data
- **Historical Analysis**: Weather pattern analysis over time
- **Real-time Updates**: Live data refresh every 5 minutes
- **Multi-city Comparison**: Side-by-side weather comparisons
- **Alert History**: Comprehensive alert tracking and resolution

## 🛠️ Enhanced Tech Stack

### **Backend Services**
- **FastAPI 0.104**: High-performance async API framework
- **WebSockets**: Real-time bidirectional communication
- **PostgreSQL 15**: Robust relational database with user/weather data
- **Redis 7**: Caching, session management, and pub/sub messaging
- **JWT Authentication**: Secure token-based authentication
- **Prometheus Client**: Metrics collection and monitoring

### **Frontend Application**
- **React 18.2**: Modern component-based UI framework
- **Leaflet.js**: Interactive mapping and geolocation
- **Recharts**: Beautiful, responsive data visualization
- **React Router**: Client-side routing and navigation
- **Axios**: HTTP client for API communication
- **React Toastify**: User-friendly notification system

### **Infrastructure & DevOps**
- **Docker Compose**: Multi-container orchestration
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Advanced dashboards and visualization
- **Node Exporter**: System metrics collection
- **AlertManager**: Alert routing and management
- **APScheduler**: Automated weather data fetching

### **External Integrations**
- **OpenWeatherMap API**: Weather and air quality data
- **SMTP Email Service**: Email notification delivery
- **Twilio SMS**: Text message alert delivery
- **Reverse Geocoding**: Location name resolution

## 📦 Enhanced Project Structure

```
weather-monitoring-system/
├── backend/                          # FastAPI Backend Service
│   ├── app/
│   │   ├── api/                     # REST API endpoints
│   │   │   ├── auth.py              # Authentication routes
│   │   │   ├── weather.py           # Weather data endpoints
│   │   │   ├── alerts.py            # Alert management
│   │   │   └── user_alerts.py       # User custom alerts
│   │   ├── core/                    # Core functionality
│   │   │   ├── config.py            # Configuration settings
│   │   │   ├── database.py          # Database connection
│   │   │   ├── security.py          # JWT authentication
│   │   │   └── metrics.py           # Prometheus metrics
│   │   ├── models/                  # Database models
│   │   │   ├── weather.py           # Weather & alert models
│   │   │   └── user.py              # User & custom alert models
│   │   ├── services/                # Business logic
│   │   │   ├── weather_service.py   # Weather data processing
│   │   │   └── notification_service.py # Email/SMS notifications
│   │   └── websocket/               # Real-time communication
│   │       └── manager.py           # WebSocket connection manager
│   ├── requirements.txt             # Python dependencies
│   └── Dockerfile                   # Backend container config
├── frontend/                        # React Frontend Application
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── WeatherDashboard.js  # Main dashboard
│   │   │   ├── AlertPanel.js        # Alert management
│   │   │   ├── MapSelector.js       # Interactive map
│   │   │   ├── Login.js             # Authentication
│   │   │   └── Register.js          # User registration
│   │   ├── services/                # API communication
│   │   │   └── api.js               # HTTP client
│   │   ├── hooks/                   # Custom React hooks
│   │   │   └── useWebSocket.js      # WebSocket hook
│   │   └── App.js                   # Main application
│   ├── package.json                 # Node.js dependencies
│   └── Dockerfile                   # Frontend container config
├── scheduler/                       # Weather Data Scheduler
│   ├── weather_scheduler.py         # Automated data fetching
│   ├── requirements.txt             # Python dependencies
│   └── Dockerfile                   # Scheduler container config
├── monitoring/                      # Monitoring Configuration
│   ├── prometheus.yml               # Prometheus config
│   ├── alert_rules.yml              # Alerting rules
│   └── alertmanager.yml             # Alert manager config
├── docker-compose.yml               # Multi-service orchestration
├── .env.example                     # Environment template
└── README.md                        # Project documentation
```

## 🚀 Quick Start Guide

### **Prerequisites**
- Docker & Docker Compose installed
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))
- Optional: Gmail app password for email alerts
- Optional: Twilio account for SMS alerts

### **1. Environment Setup**
```bash
# Clone the repository
git clone <repository-url>
cd weather-monitoring-system

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

### **2. Required Configuration**
```bash
# Minimum required in .env file:
OPENWEATHER_API_KEY=your_openweathermap_api_key_here

# Optional for notifications:
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone
```

### **3. Launch the System**
```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### **4. Access the Services**
- **🌤️ Main Dashboard**: http://localhost:3000
- **📚 API Documentation**: http://localhost:8000/docs
- **📊 Grafana Monitoring**: http://localhost:3001 (admin/admin)
- **🔍 Prometheus Metrics**: http://localhost:9090
- **⚡ System Metrics**: http://localhost:8000/metrics

## 🔧 Comprehensive Configuration

### **Environment Variables**

#### **Core Services**
```bash
# Weather API (Required)
OPENWEATHER_API_KEY=your_api_key_here

# Database
DATABASE_URL=postgresql://weather_user:weather_pass@postgres:5432/weather_monitoring

# Redis Cache
REDIS_URL=redis://redis:6379
```

#### **Alert Thresholds**
```bash
TEMP_HIGH_THRESHOLD=45.0      # High temperature alert (°C)
TEMP_LOW_THRESHOLD=-10.0      # Low temperature alert (°C)
HUMIDITY_HIGH_THRESHOLD=90.0  # High humidity alert (%)
AQI_HIGH_THRESHOLD=150        # Poor air quality alert
```

#### **Email Notifications**
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

#### **SMS Notifications**
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

## 🎯 User Guide

### **Getting Started**
1. **Sign Up**: Create your account at http://localhost:3000
2. **Add Cities**: Use the interactive map to select monitoring locations
3. **Set Alerts**: Configure personal thresholds for temperature, humidity, AQI
4. **Monitor**: View real-time data and receive instant notifications

### **Key Features Usage**

#### **Interactive Map**
- Click anywhere on the map to add a new monitoring location
- View real-time weather markers with current conditions
- Manage your saved cities and favorites

#### **Custom Alerts**
- Set personalized thresholds for each city
- Choose notification preferences (email/SMS)
- View alert history and resolution status

#### **Dashboard Analytics**
- Monitor temperature trends over time
- Compare weather data across multiple cities
- Track system performance and alert statistics

## 📊 Monitoring & Observability

### **Grafana Dashboards**
Access comprehensive monitoring at http://localhost:3001:
- **System Health**: CPU, memory, disk usage
- **API Performance**: Request rates, response times, errors
- **Weather Metrics**: Data fetch success rates, alert counts
- **User Activity**: Authentication, city additions, alert configurations

### **Prometheus Metrics**
Key metrics available at http://localhost:9090:
- `weather_api_requests_total` - API request counts
- `weather_api_request_duration_seconds` - Response times
- `weather_fetch_total` - Weather data fetch attempts
- `weather_alerts_total` - Generated alerts by type
- `weather_websocket_connections_active` - Active connections

### **Alert Rules**
Automated system alerts for:
- High API error rates (>10% for 2 minutes)
- Slow response times (>2 seconds for 5 minutes)
- Weather fetch failures (>20% for 5 minutes)
- High system resource usage (CPU >80%, Memory >85%)

## 🔌 API Reference

### **Authentication Endpoints**
```bash
POST /api/auth/register    # User registration
POST /api/auth/login       # User login
GET  /api/auth/me          # Get user profile
```

### **Weather Data Endpoints**
```bash
GET  /api/weather/current/{city}     # Current weather
GET  /api/weather/history/{city}     # Historical data
GET  /api/weather/latest             # Latest readings
```

### **Alert Management**
```bash
GET  /api/alerts/                    # Get alerts
PUT  /api/alerts/{id}/resolve        # Resolve alert
GET  /api/alerts/stats               # Alert statistics
```

### **User Management**
```bash
POST /api/user/cities                # Add user city
GET  /api/user/cities                # Get user cities
POST /api/user/alerts                # Create custom alert
GET  /api/user/alerts                # Get user alerts
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Services Won't Start**
```bash
# Check Docker status
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend
```

#### **Database Connection Issues**
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
docker-compose up backend
```

#### **API Key Issues**
- Verify OpenWeatherMap API key is valid
- Check API key has sufficient quota
- Ensure .env file is properly formatted

#### **Notification Issues**
- For Gmail: Use app-specific password, not regular password
- For Twilio: Verify account SID and auth token
- Check phone number format (+1234567890)

## 🔒 Security Considerations

- **JWT Tokens**: Secure authentication with configurable expiration
- **Password Hashing**: Bcrypt encryption for user passwords
- **API Rate Limiting**: Built-in protection against abuse
- **CORS Configuration**: Controlled cross-origin access
- **Environment Variables**: Sensitive data stored securely

## 🚀 Production Deployment

### **Docker Swarm**
```bash
docker swarm init
docker stack deploy -c docker-compose.yml weather-stack
```

### **Kubernetes**
```bash
# Convert docker-compose to k8s manifests
kompose convert
kubectl apply -f .
```

### **Cloud Deployment**
- **AWS**: Use ECS/EKS with RDS and ElastiCache
- **GCP**: Deploy on GKE with Cloud SQL and Memorystore
- **Azure**: Use AKS with Azure Database and Redis Cache