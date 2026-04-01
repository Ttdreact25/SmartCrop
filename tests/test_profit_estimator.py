"""Tests for smart_crop.profit_estimator module."""
import pytest
from smart_crop.profit_estimator import ProfitEstimator


class TestProfitEstimator:
    """Test cases for ProfitEstimator class."""

    def test_init(self):
        """Test ProfitEstimator initialization."""
        estimator = ProfitEstimator()
        assert estimator is not None

    def test_estimate_profit(self):
        """Test profit estimation."""
        estimator = ProfitEstimator()
        crop_data = {
            'crop': 'rice',
            'area_hectares': 1.0,
            'expected_yield_tons': 4.0,
            'market_price_per_ton': 500
        }
        result = estimator.estimate_profit(crop_data)
        assert result is not None
        assert 'estimated_revenue' in result
        assert 'estimated_cost' in result
        assert 'estimated_profit' in result
        assert isinstance(result['estimated_revenue'], (int, float))
        assert isinstance(result['estimated_cost'], (int, float))
        assert isinstance(result['estimated_profit'], (int, float))

    def test_compare_crops(self):
        """Test crop comparison."""
        estimator = ProfitEstimator()
        crops = [
            {'crop': 'rice', 'area_hectares': 1.0, 'expected_yield_tons': 4.0, 'market_price_per_ton': 500},
            {'crop': 'wheat', 'area_hectares': 1.0, 'expected_yield_tons': 3.0, 'market_price_per_ton': 400}
        ]
        comparison = estimator.compare_crops(crops)
        assert comparison is not None
        assert isinstance(comparison, list)
        assert len(comparison) == 2
