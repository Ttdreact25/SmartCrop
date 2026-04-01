"""Tests for smart_crop.equipment_recommender module."""
import pytest
from smart_crop.equipment_recommender import EquipmentRecommender


class TestEquipmentRecommender:
    """Test cases for EquipmentRecommender class."""

    def test_init(self):
        """Test EquipmentRecommender initialization."""
        recommender = EquipmentRecommender()
        assert recommender is not None

    def test_get_equipment_recommendations(self):
        """Test getting equipment recommendations."""
        recommender = EquipmentRecommender()
        crop = 'rice'
        area = 1.0
        recommendations = recommender.get_equipment_recommendations(crop, area)
        assert recommendations is not None
        assert isinstance(recommendations, list)

    def test_get_equipment_details(self):
        """Test getting equipment details."""
        recommender = EquipmentRecommender()
        equipment_name = 'tractor'
        details = recommender.get_equipment_details(equipment_name)
        assert details is not None
        assert isinstance(details, dict)

    def test_calculate_equipment_cost(self):
        """Test calculating equipment cost."""
        recommender = EquipmentRecommender()
        equipment = ['tractor', 'harvester']
        duration_days = 30
        cost = recommender.calculate_equipment_cost(equipment, duration_days)
        assert cost is not None
        assert isinstance(cost, (int, float))
        assert cost >= 0
