# tests/test_display_controller.py

import pytest
from src.controllers import DisplayController
from src.utils import DisplayControlError

@pytest.fixture
def display_controller():
    return DisplayController()

def test_get_display_info(display_controller):
    info = display_controller.get_display_info()
    assert isinstance(info, list)
    assert all(isinstance(display, dict) for display in info)
    assert all('id' in display and 'name' in display and 'resolution' in display and 'refresh_rate' in display for display in info)

def test_set_resolution(display_controller):
    result = display_controller.set_resolution(0, 1920, 1080)
    assert result == {"status": "success", "message": "Resolution set to 1920x1080"}

def test_set_refresh_rate(display_controller):
    result = display_controller.set_refresh_rate(0, 60)
    assert result == {"status": "success", "message": "Refresh rate set to 60Hz"}

def test_enable_dummy_display(display_controller):
    result = display_controller.enable_dummy_display()
    assert result == {"status": "success", "message": "Dummy display enabled"}

def test_disable_dummy_display(display_controller):
    result = display_controller.disable_dummy_display()
    assert result == {"status": "success", "message": "Dummy display disabled"}

# Add more tests for error cases