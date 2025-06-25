import pytest
from dashboard.utils import load_config  # Adjust as needed

def test_valid_config():
    config = load_config("tests/test_data/valid_config.json")
    assert isinstance(config, dict)
    assert "widgets" in config

def test_invalid_config():
    with pytest.raises(Exception):
        load_config("tests/test_data/invalid_config.json")