import pytest
from smart_crop.organic_farming import NATURAL_FERTILIZERS, ORGANIC_PESTICIDES, COMPOSTING_TIPS


def test_natural_fertilizers_data():
    """Test that NATURAL_FERTILIZERS contains expected data."""
    assert isinstance(NATURAL_FERTILIZERS, dict)
    assert len(NATURAL_FERTILIZERS) > 0
    assert "Vermicompost" in NATURAL_FERTILIZERS
    assert "Neem Cake" in NATURAL_FERTILIZERS


def test_fertilizer_structure():
    """Test the structure of fertilizer data."""
    fertilizer = NATURAL_FERTILIZERS["Vermicompost"]
    required_keys = ["description", "nutrients", "application", "benefits", "preparation", "cost"]
    for key in required_keys:
        assert key in fertilizer
        assert isinstance(fertilizer[key], (str, list))


def test_organic_pesticides_data():
    """Test that ORGANIC_PESTICIDES contains expected data."""
    assert isinstance(ORGANIC_PESTICIDES, dict)
    assert len(ORGANIC_PESTICIDES) > 0
    assert "Neem Oil" in ORGANIC_PESTICIDES


def test_pesticide_structure():
    """Test the structure of pesticide data."""
    pesticide = ORGANIC_PESTICIDES["Neem Oil"]
    required_keys = ["description", "targets", "preparation", "application", "safety"]
    for key in required_keys:
        assert key in pesticide
        assert isinstance(pesticide[key], str)


def test_composting_tips():
    """Test composting tips data."""
    assert isinstance(COMPOSTING_TIPS, dict)
    assert "Basic Composting" in COMPOSTING_TIPS
    composting = COMPOSTING_TIPS["Basic Composting"]
    assert "materials" in composting
    assert "steps" in composting
    assert "tips" in composting