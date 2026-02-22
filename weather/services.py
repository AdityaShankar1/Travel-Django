import requests

CITY_COORDINATES = {
    'Chennai': {'lat': 13.0827, 'lon': 80.2707},
    'Madurai': {'lat': 9.9252, 'lon': 78.1198},
    'Trichy': {'lat': 10.7905, 'lon': 78.7047},
    'Coimbatore': {'lat': 11.0168, 'lon': 76.9558},
    'Tuticorin': {'lat': 8.7642, 'lon': 78.1348},
}

def get_weather_data():
    """
    Fetches real-time weather data for the top 5 cities in Tamil Nadu.
    """
    weather_results = []
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    for city, coords in CITY_COORDINATES.items():
        params = {
            "latitude": coords['lat'],
            "longitude": coords['lon'],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m",
            "timezone": "auto"
        }
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            current = data.get('current', {})
            
            weather_results.append({
                'city': city,
                'lat': coords['lat'],
                'lon': coords['lon'],
                'temp': current.get('temperature_2m'),
                'humidity': current.get('relative_humidity_2m'),
                'feels_like': current.get('apparent_temperature'),
                'wind_speed': current.get('wind_speed_10m'),
                'weather_code': current.get('weather_code'),
                'condition': _get_weather_condition(current.get('weather_code'))
            })
        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")
            weather_results.append({
                'city': city,
                'lat': coords['lat'],
                'lon': coords['lon'],
                'error': True
            })
            
    return weather_results

def _get_weather_condition(code):
    """
    Maps WMO Weather interpretation codes to human-readable strings.
    """
    mapping = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return mapping.get(code, "Unknown")
