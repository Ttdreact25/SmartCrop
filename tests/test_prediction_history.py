"""Tests for smart_crop.prediction_history module."""
import pytest
from smart_crop.prediction_history import PredictionHistory


class TestPredictionHistory:
    """Test cases for PredictionHistory class."""

    def test_init(self):
        """Test PredictionHistory initialization."""
        history = PredictionHistory()
        assert history is not None

    def test_add_prediction(self):
        """Test adding a prediction to history."""
        history = PredictionHistory()
        prediction = {
            'crop': 'rice',
            'confidence': 0.95,
            'timestamp': '2024-01-01T12:00:00'
        }
        result = history.add_prediction(prediction)
        assert result is True

    def test_get_history(self):
        """Test getting prediction history."""
        history = PredictionHistory()
        prediction = {
            'crop': 'rice',
            'confidence': 0.95,
            'timestamp': '2024-01-01T12:00:00'
        }
        history.add_prediction(prediction)
        history_list = history.get_history()
        assert history_list is not None
        assert isinstance(history_list, list)
        assert len(history_list) >= 1

    def test_clear_history(self):
        """Test clearing prediction history."""
        history = PredictionHistory()
        prediction = {
            'crop': 'rice',
            'confidence': 0.95,
            'timestamp': '2024-01-01T12:00:00'
        }
        history.add_prediction(prediction)
        result = history.clear_history()
        assert result is True
        assert len(history.get_history()) == 0
