import pytest
from smart_crop.storage_tips import CROP_STORAGE_DATA


def test_crop_storage_data():
    """Test that CROP_STORAGE_DATA contains expected data."""
    assert isinstance(CROP_STORAGE_DATA, dict)
    assert len(CROP_STORAGE_DATA) > 0
    assert "Rice" in CROP_STORAGE_DATA
    assert "Wheat" in CROP_STORAGE_DATA


def test_storage_structure():
    """Test the structure of storage data."""
    storage = CROP_STORAGE_DATA["Rice"]
    required_keys = ["storage_method", "ideal_temperature", "ideal_humidity", "shelf_life", "storage_tips", "spoilage_signs", "prevention_tips", "best_practices"]
    for key in required_keys:
        assert key in storage
        if key.endswith("tips"):
            assert isinstance(storage[key], list)
        else:
            assert isinstance(storage[key], str)