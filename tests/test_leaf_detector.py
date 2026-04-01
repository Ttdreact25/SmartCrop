"""Tests for smart_crop.leaf_detector module."""
import pytest
import numpy as np
from smart_crop.leaf_detector import LeafDetector


class TestLeafDetector:
    """Test cases for LeafDetector class."""

    def test_init(self):
        """Test LeafDetector initialization."""
        detector = LeafDetector()
        assert detector is not None
        assert hasattr(detector, 'model')

    def test_detect_disease(self):
        """Test leaf disease detection."""
        detector = LeafDetector()
        # Create a dummy image (numpy array)
        image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        result = detector.detect_disease(image)
        assert result is not None
        assert 'disease' in result
        assert 'confidence' in result
        assert isinstance(result['disease'], str)
        assert isinstance(result['confidence'], (int, float))

    def test_get_disease_info(self):
        """Test getting disease information."""
        detector = LeafDetector()
        disease = 'late_blight'
        info = detector.get_disease_info(disease)
        assert info is not None
        assert 'name' in info
        assert 'symptoms' in info
        assert 'treatment' in info

    def test_preprocess_image(self):
        """Test image preprocessing."""
        detector = LeafDetector()
        image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
        processed = detector.preprocess_image(image)
        assert processed is not None
        assert processed.shape == (224, 224, 3)
