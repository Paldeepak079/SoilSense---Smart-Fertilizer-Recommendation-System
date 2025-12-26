"""
Weather service for fertilizer application timing
Uses free weather API (Open-Meteo) - no API key needed
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class WeatherService:
    """Get weather forecast for fertilizer timing recommendations"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    @staticmethod
    def get_forecast(latitude: float, longitude: float, days: int = 7) -> Optional[Dict]:
        """
        Get weather forecast for location
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days: Forecast days (default 7)
        
        Returns:
            Weather forecast data or None if API fails
        """
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum',
                'timezone': 'Asia/Kolkata',
                'forecast_days': days
            }
            
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    @staticmethod
    def get_fertilizer_timing_advice(latitude: float, longitude: float) -> str:
        """
        Get fertilizer application timing advice based on weather
        
        Returns:
            Timing advice string
        """
        forecast = WeatherService.get_forecast(latitude, longitude, days=7)
        
        if not forecast or 'daily' not in forecast:
            return "Weather data unavailable. Apply based on standard schedule."
        
        daily = forecast['daily']
        rain_forecast = daily.get('rain_sum', [])
        
        # Check next 3 days for rain
        advice = []
        rainy_days = sum(1 for rain in rain_forecast[:3] if rain > 5)  # >5mm is significant
        
        if rainy_days >= 2:
            advice.append("⚠️ Heavy rain expected in next 3 days")
            advice.append("Postpone top dressing application")
            advice.append("Wait for dry weather to prevent nutrient loss")
        elif rainy_days == 1:
            advice.append("🌦️ Light rain expected")
            advice.append("Safe to apply basal fertilizers")
            advice.append("Delay top dressing by 2-3 days")
        else:
            advice.append("☀️ Good weather for fertilizer application")
            advice.append("Apply as per schedule")
            advice.append("Irrigate after top dressing if no rain expected")
        
        return " | ".join(advice)


# District coordinates (for weather lookup)
DISTRICT_COORDINATES = {
    'Pune': {'lat': 18.5204, 'lon': 73.8567},
    'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
    'Nagpur': {'lat': 21.1458, 'lon': 79.0882},
    'Nashik': {'lat': 19.9975, 'lon': 73.7898},
    'Amravati': {'lat': 20.9374, 'lon': 77.7796},
    # Add more districts as needed
    'Delhi': {'lat': 28.6139, 'lon': 77.2090},
    'Ludhiana': {'lat': 30.9010, 'lon': 75.8573},
    'Chandigarh': {'lat': 30.7333, 'lon': 76.7794},
}


def get_location_coords(district: str) -> tuple:
    """Get coordinates for district, return default if not found"""
    coords = DISTRICT_COORDINATES.get(district, {'lat': 20.5937, 'lon': 78.9629})  # India center
    return coords['lat'], coords['lon']
