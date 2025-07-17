# WeatherPulse API Documentation

## 🔗 Base URL
```
http://localhost:8000
```

## 🔐 Authentication

WeatherPulse uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

## 📚 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true
}
```

#### Login User
```http
POST /api/auth/login
```

**Request Body (Form Data):**
```
username: user@example.com
password: your_password
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/auth/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "is_active": true
}
```

### Weather Data Endpoints

#### Get Current Weather
```http
GET /api/weather/current/{city}
```

**Parameters:**
- `city` (path): City name (e.g., "New York", "London")

**Response:**
```json
{
  "id": 1,
  "city": "New York",
  "temperature": 22.5,
  "humidity": 65.0,
  "pressure": 1013.25,
  "aqi": 45,
  "weather_condition": "Clear",
  "timestamp": "2025-01-17T10:30:00Z"
}
```

#### Get Weather History
```http
GET /api/weather/history/{city}?hours=24&limit=100
```

**Parameters:**
- `city` (path): City name
- `hours` (query): Number of hours to look back (default: 24)
- `limit` (query): Maximum number of records (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "city": "New York",
    "temperature": 22.5,
    "humidity": 65.0,
    "pressure": 1013.25,
    "aqi": 45,
    "weather_condition": "Clear",
    "timestamp": "2025-01-17T10:30:00Z"
  }
]
```

#### Get Latest Readings
```http
GET /api/weather/latest?limit=10
```

**Parameters:**
- `limit` (query): Number of latest readings (default: 10)

**Response:**
```json
[
  {
    "id": 1,
    "city": "New York",
    "temperature": 22.5,
    "humidity": 65.0,
    "pressure": 1013.25,
    "aqi": 45,
    "weather_condition": "Clear",
    "timestamp": "2025-01-17T10:30:00Z"
  }
]
```

### Alert Management Endpoints

#### Get Alerts
```http
GET /api/alerts/?city=New York&alert_type=temperature&resolved=false&hours=24&limit=50
```

**Parameters:**
- `city` (query): Filter by city name
- `alert_type` (query): Filter by alert type (temperature, humidity, aqi)
- `resolved` (query): Filter by resolution status (true/false)
- `hours` (query): Hours to look back (default: 24)
- `limit` (query): Maximum number of alerts (default: 50)

**Response:**
```json
[
  {
    "id": 1,
    "alert_type": "temperature",
    "threshold_value": 45.0,
    "actual_value": 47.2,
    "city": "New York",
    "message": "High temperature alert: 47.2°C in New York",
    "is_resolved": false,
    "created_at": "2025-01-17T10:30:00Z",
    "resolved_at": null
  }
]
```

#### Resolve Alert
```http
PUT /api/alerts/{alert_id}/resolve
```

**Parameters:**
- `alert_id` (path): Alert ID to resolve

**Response:**
```json
{
  "message": "Alert resolved successfully"
}
```

#### Get Alert Statistics
```http
GET /api/alerts/stats?hours=24
```

**Parameters:**
- `hours` (query): Hours to look back (default: 24)

**Response:**
```json
{
  "total_alerts": 15,
  "resolved_alerts": 8,
  "unresolved_alerts": 7,
  "by_type": {
    "temperature": 10,
    "humidity": 3,
    "aqi": 2
  }
}
```

### User Management Endpoints

#### Add User City
```http
POST /api/user/cities
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "city": "Tokyo",
  "latitude": 35.6762,
  "longitude": 139.6503,
  "is_favorite": false
}
```

**Response:**
```json
{
  "id": 1,
  "city": "Tokyo",
  "latitude": 35.6762,
  "longitude": 139.6503,
  "is_favorite": false
}
```

#### Get User Cities
```http
GET /api/user/cities
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "city": "Tokyo",
    "latitude": 35.6762,
    "longitude": 139.6503,
    "is_favorite": false
  }
]
```

#### Delete User City
```http
DELETE /api/user/cities/{city_id}
```

**Parameters:**
- `city_id` (path): City ID to delete

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "City removed successfully"
}
```

#### Create Custom Alert
```http
POST /api/user/alerts
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "city": "New York",
  "alert_type": "temperature",
  "threshold_value": 40.0,
  "email_enabled": true,
  "sms_enabled": false
}
```

**Response:**
```json
{
  "id": 1,
  "city": "New York",
  "alert_type": "temperature",
  "threshold_value": 40.0,
  "is_active": true,
  "email_enabled": true,
  "sms_enabled": false
}
```

#### Get User Alerts
```http
GET /api/user/alerts
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "city": "New York",
    "alert_type": "temperature",
    "threshold_value": 40.0,
    "is_active": true,
    "email_enabled": true,
    "sms_enabled": false
  }
]
```

#### Update Custom Alert
```http
PUT /api/user/alerts/{alert_id}
```

**Parameters:**
- `alert_id` (path): Alert ID to update

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "city": "New York",
  "alert_type": "temperature",
  "threshold_value": 45.0,
  "email_enabled": true,
  "sms_enabled": true
}
```

**Response:**
```json
{
  "message": "Alert updated successfully"
}
```

#### Delete Custom Alert
```http
DELETE /api/user/alerts/{alert_id}
```

**Parameters:**
- `alert_id` (path): Alert ID to delete

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Alert deleted successfully"
}
```

## 🔌 WebSocket Connection

### Connect to WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
  const alertData = JSON.parse(event.data);
  console.log('New alert:', alertData);
};
```

### WebSocket Message Format
```json
{
  "id": 1,
  "type": "temperature",
  "message": "High temperature alert: 47.2°C in New York",
  "city": "New York",
  "timestamp": "2025-01-17T10:30:00Z"
}
```

## 📊 Monitoring Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

#### Prometheus Metrics
```http
GET /metrics
```

**Response:**
```
# HELP weather_api_requests_total Total number of API requests
# TYPE weather_api_requests_total counter
weather_api_requests_total{method="GET",endpoint="/api/weather/current/New York",status_code="200"} 42.0
```

## 🚨 Error Responses

### Common Error Codes

#### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## 📝 Rate Limiting

- **Authentication endpoints**: 5 requests per minute
- **Weather data endpoints**: 100 requests per minute
- **User management endpoints**: 50 requests per minute

## 🔧 SDK Examples

### Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login', data={
    'username': 'user@example.com',
    'password': 'password'
})
token = response.json()['access_token']

# Get weather data
headers = {'Authorization': f'Bearer {token}'}
weather = requests.get('http://localhost:8000/api/weather/current/New York', headers=headers)
print(weather.json())
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=user@example.com&password=password'
});
const { access_token } = await loginResponse.json();

// Get weather data
const weatherResponse = await fetch('/api/weather/current/New York', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const weather = await weatherResponse.json();
console.log(weather);
```

### cURL
```bash
# Login
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password" | jq -r '.access_token')

# Get weather data
curl -X GET "http://localhost:8000/api/weather/current/New York" \
  -H "Authorization: Bearer $TOKEN"
```

## 🔍 Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly in your browser.