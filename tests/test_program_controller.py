# tests/test_program_controller.py

import pytest
from unittest.mock import patch, MagicMock
from src.controllers import ProgramController
from src.utils import ProgramControlError

@pytest.fixture
def program_controller():
    return ProgramController()

@patch('psutil.process_iter')
def test_get_running_programs(mock_process_iter, program_controller):
    mock_process = MagicMock()
    mock_process.info = {'pid': 1234, 'name': 'test_program'}
    mock_process_iter.return_value = [mock_process]
    
    programs = program_controller.get_running_programs()
    assert programs == [{'pid': 1234, 'name': 'test_program'}]

@patch('psutil.Process')
def test_pause_program(mock_process, program_controller):
    mock_process_instance = MagicMock()
    mock_process.return_value = mock_process_instance
    
    result = program_controller.pause_program(1234)
    mock_process_instance.suspend.assert_called_once()
    assert result == {"status": "success", "message": "Program with PID 1234 paused"}

@patch('psutil.Process')
def test_resume_program(mock_process, program_controller):
    mock_process_instance = MagicMock()
    mock_process.return_value = mock_process_instance
    
    result = program_controller.resume_program(1234)
    mock_process_instance.resume.assert_called_once()
    assert result == {"status": "success", "message": "Program with PID 1234 resumed"}

@patch('psutil.Process', side_effect=Exception("Test error"))
def test_pause_program_error(mock_process, program_controller):
    with pytest.raises(ProgramControlError):
        program_controller.pause_program(1234)

# Add more tests for error cases