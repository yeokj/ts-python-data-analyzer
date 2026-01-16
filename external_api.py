import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_hourly_temperature(latitude, longitude, timezone="auto"):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "timezone": timezone,
        "forecast_days": 1,
    }
    
    response = requests.get(OPEN_METEO_URL, params=params)
    response.raise_for_status()
    data = response.json()
    print(data.get('hourly', {}))

    hourly = data.get('hourly', {})
    times = hourly.get('time', [])
    temperatures = hourly.get('temperature_2m', [])

    # Extract temperature unit
    hourly_units = data.get('hourly_units', {})
    temperature_unit = hourly_units.get('temperature_2m', '°C')  # Default to Celsius

    return times, temperatures, temperature_unit

    # return response.json()