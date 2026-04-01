"""Tests for smart_crop.data_loader module."""
import pytest
import pandas as pd
from smart_crop.data_loader import load_crop_data, load_location_data


def test_load_crop_data():
    """Test loading crop data."""
    df = load_crop_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_location_data():
    """Test loading location data."""
    df = load_location_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
        loader = DataLoader()
        assert loader is not None

    def test_load_crop_data(self):
        """Test loading crop data."""
        loader = DataLoader()
        data = loader.load_crop_data()
        assert data is not None
        assert isinstance(data, (list, dict))

    def test_load_weather_data(self):
        """Test loading weather data."""
        loader = DataLoader()
        data = loader.load_weather_data()
        assert data is not None
        assert isinstance(data, (list, dict))

    def test_load_soil_data(self):
        """Test loading soil data."""
        loader = DataLoader()
        data = loader.load_soil_data()
        assert data is not None
        assert isinstance(data, (list, dict))
