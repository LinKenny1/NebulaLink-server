# tests/test_power_controller.py

import pytest
from unittest.mock import patch, MagicMock
from src.controllers import PowerController
from src.utils import PowerControlError


@pytest.fixture
def power_controller():
    return PowerController()


def test_get_power_plans(power_controller):
    plans = power_controller.get_power_plans()
    assert isinstance(plans, list)
    assert all(isinstance(plan, dict) for plan in plans)
    assert all("guid" in plan and "name" in plan for plan in plans)


@patch("subprocess.run", side_effect=Exception("Test error"))
def test_set_power_plan_error(mock_run, power_controller):
    with pytest.raises(PowerControlError) as exc_info:
        power_controller.set_power_plan("test-guid")
    assert "Unexpected error while setting power plan: Test error" in str(
        exc_info.value
    )


@patch("subprocess.run", side_effect=Exception("Test error"))
def test_set_power_plan_error(mock_run, power_controller):
    with pytest.raises(PowerControlError):
        power_controller.set_power_plan("test-guid")


# Add more tests for shutdown, restart, sleep, and hibernate methods
