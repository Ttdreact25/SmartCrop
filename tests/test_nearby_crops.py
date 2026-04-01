"""Tests for smart_crop.nearby_crops module."""
import pytest
from smart_crop.nearby_crops import NearbyCrops


class TestNearbyCrops:
    """Test cases for NearbyCrops class."""

    def test_init(self):
        """Test NearbyCrops initialization."""
        nearby = NearbyCrops()
        assert nearby is not None

    def test_get_nearby_crops(self):
        """Test getting nearby crops."""
        nearby = NearbyCrops()
        location = {'lat': 28.6139, 'lon': 77.2090}
        crops = nearby.get_nearby_crops(location, radius_km=50)
        assert crops is not None
        assert isinstance(crops, list)

    def test_get_crop_distribution(self):
        """Test getting crop distribution."""
        nearby = NearbyCrops()
        location = {'lat': 28.6139, 'lon': 77.2090}
        distribution = nearby.get_crop_distribution(location, radius_km=50)
        assert distribution is not None
        assert isinstance(distribution, dict)

    def test_get_popular_crops(self):
        """Test getting popular crops in area."""
        nearby = NearbyCrops()
        location = {'lat': 28.6139, 'lon': 77.2090}
        popular = nearby.get_popular_crops(location, radius_km=50, top_n=5)
        assert popular is not None
        assert isinstance(popular, list)
        assert len(popular) <= 5
