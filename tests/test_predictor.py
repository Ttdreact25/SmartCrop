"""Tests for smart_crop.predictor module."""
import pytest
import numpy as np
from smart_crop.predictor import CropPredictor


class TestCropPredictor:
    """Test cases for CropPredictor class."""

    def test_init(self):
        """Test CropPredictor initialization."""
        predictor = CropPredictor()
        assert predictor is not None
        assert hasattr(predictor, 'model')
        assert hasattr(predictor, 'scaler')

    def test_predict(self):
        """Test crop prediction."""
        predictor = CropPredictor()
        # Sample input features
        features = {
            'N': 90,
            'P': 42,
            'K': 43,
            'temperature': 20.87,
            'humidity': 82.00,
            'ph': 6.5,
            'rainfall': 202.93
        }
        result = predictor.predict(features)
        assert result is not None
        assert 'crop' in result
        assert 'confidence' in result
        assert isinstance(result['crop'], str)
        assert isinstance(result['confidence'], (int, float))

    def test_get_crop_recommendations(self):
        """Test getting crop recommendations."""
        predictor = CropPredictor()
        features = {
            'N': 90,
            'P': 42,
            'K': 43,
            'temperature': 20.87,
            'humidity': 82.00,
            'ph': 6.5,
            'rainfall': 202.93
        }
        recommendations = predictor.get_crop_recommendations(features, top_n=3)
        assert recommendations is not None
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3
        for rec in recommendations:
            assert 'crop' in rec
            assert 'confidence' in rec
