import pytest
from core.api_client import fetch_weather, fetch_forecast

def test_fetch_weather_valid_city():
    data = fetch_weather("New York")
    assert "main" in data
    assert "weather" in data

def test_fetch_weather_invalid_city():
    with pytest.raises(Exception):
        fetch_weather("Nocityxyz")

def test_fetch_forecast_valid_city():
    data = fetch_forecast("Los Angeles")
    assert "list" in data
    assert len(data["list"]) > 0
