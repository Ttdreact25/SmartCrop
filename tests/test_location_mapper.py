"""Tests for smart_crop.location_mapper module."""
import pytest
from smart_crop.location_mapper import LocationMapper


class TestLocationMapper:
    """Test cases for LocationMapper class."""

    def test_init(self):
        """Test LocationMapper initialization."""
        mapper = LocationMapper()
        assert mapper is not None

    def test_get_coordinates(self):
        """Test getting coordinates from location name."""
        mapper = LocationMapper()
        location = 'New Delhi, India'
        coords = mapper.get_coordinates(location)
        assert coords is not None
        assert 'lat' in coords
        assert 'lon' in coords
        assert isinstance(coords['lat'], (int, float))
        assert isinstance(coords['lon'], (int, float))

    def test_get_location_from_coordinates(self):
        """Test getting location name from coordinates."""
        mapper = LocationMapper()
        lat = 28.6139
        lon = 77.2090
        location = mapper.get_location_from_coordinates(lat, lon)
        assert location is not None
        assert isinstance(location, str)

    def test_get_nearby_locations(self):
        """Test getting nearby locations."""
        mapper = LocationMapper()
        lat = 28.6139
        lon = 77.2090
        nearby = mapper.get_nearby_locations(lat, lon, radius_km=50)
        assert nearby is not None
        assert isinstance(nearby, list)
