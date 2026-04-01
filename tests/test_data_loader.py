"""Tests for smart_crop.data_loader module."""
import pytest
from smart_crop.data_loader import DataLoader


class TestDataLoader:
    """Test cases for DataLoader class."""

    def test_init(self):
        """Test DataLoader initialization."""
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
