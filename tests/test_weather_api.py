"""Tests for smart_crop.weather_api module."""
import pytest
from smart_crop.weather_api import WeatherAPI


class TestWeatherAPI:
    """Test cases for WeatherAPI class."""

    def test_init(self):
        """Test WeatherAPI initialization."""
        api = WeatherAPI()
        assert api is not None

    def test_get_weather(self):
        """Test getting weather data."""
        api = WeatherAPI()
        location = {'lat': 28.6139, 'lon': 77.2090}
        weather = api.get_weather(location)
        assert weather is not None
        assert 'temperature' in weather
        assert 'humidity' in weather
        assert 'rainfall' in weather

    def test_get_forecast(self):
        """Test getting weather forecast."""
        api = WeatherAPI()
        location = {'lat': 28.6139, 'lon': 77.2090}
        forecast = api.get_forecast(location, days=7)
        assert forecast is not None
        assert isinstance(forecast, list)
        assert len(forecast) <= 7

    def test_get_historical_weather(self):
        """Test getting historical weather data."""
        api = WeatherAPI()
        location = {'lat': 28.6139, 'lon': 77.2090}
        historical = api.get_historical_weather(location, days=30)
        assert historical is not None
        assert isinstance(historical, list)
