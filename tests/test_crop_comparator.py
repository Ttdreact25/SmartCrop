"""Tests for smart_crop.crop_comparator module."""
import pytest
from smart_crop.crop_comparator import CropComparator


class TestCropComparator:
    """Test cases for CropComparator class."""

    def test_init(self):
        """Test CropComparator initialization."""
        comparator = CropComparator()
        assert comparator is not None

    def test_compare_crops(self):
        """Test crop comparison."""
        comparator = CropComparator()
        crops = ['rice', 'wheat', 'maize']
        comparison = comparator.compare_crops(crops)
        assert comparison is not None
        assert isinstance(comparison, dict)
        assert len(comparison) == len(crops)

    def test_get_best_crop(self):
        """Test getting best crop recommendation."""
        comparator = CropComparator()
        conditions = {
            'temperature': 25,
            'humidity': 70,
            'rainfall': 150,
            'soil_type': 'loamy'
        }
        best = comparator.get_best_crop(conditions)
        assert best is not None
        assert 'crop' in best
        assert 'score' in best

    def test_rank_crops(self):
        """Test crop ranking."""
        comparator = CropComparator()
        conditions = {
            'temperature': 25,
            'humidity': 70,
            'rainfall': 150,
            'soil_type': 'loamy'
        }
        ranking = comparator.rank_crops(conditions, top_n=5)
        assert ranking is not None
        assert isinstance(ranking, list)
        assert len(ranking) <= 5
