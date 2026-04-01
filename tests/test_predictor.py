"""Tests for smart_crop.predictor module."""
import pytest
from smart_crop.predictor import load_crop_duration_data, predict_crop


def test_load_crop_duration_data():
    """Test loading crop duration data."""
    data = load_crop_duration_data()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_predict_crop():
    """Test crop prediction function."""
    # Mock model for testing
    class MockModel:
        def predict(self, features):
            return ["rice"]  # Mock prediction

    model = MockModel()
    features = [90, 42, 43, 20.87974371, 82.00274423, 6.502985292000001, 202.9355362]
    result = predict_crop(model, features)
    assert result == "rice"
