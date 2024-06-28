# src/utils/error_handling.py

from typing import Any, Dict
from utils.logging_config import get_logger

logger = get_logger(__name__)

class NebulaLinkError(Exception):
    """Base exception class for NebulaLink server errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ConfigurationError(NebulaLinkError):
    """Raised when there's an error in the configuration."""
    pass

class ConnectionError(NebulaLinkError):
    """Raised when there's an error establishing or maintaining a connection."""
    pass

class CommandError(NebulaLinkError):
    """Raised when there's an error executing a command."""
    pass

class PowerControlError(NebulaLinkError):
    """Raised when there's an error controlling power settings."""
    pass

class DisplayControlError(NebulaLinkError):
    """Raised when there's an error controlling display settings."""
    pass

class ProgramControlError(NebulaLinkError):
    """Raised when there's an error controlling programs."""
    pass

def handle_error(error: Exception) -> Dict[str, Any]:
    """
    Handle exceptions and return a dictionary with error details.

    Args:
        error (Exception): The exception to handle.

    Returns:
        Dict[str, Any]: A dictionary containing error details.
    """
    error_type = type(error).__name__
    error_message = str(error)
    
    logger.error(f"Error occurred: {error_type} - {error_message}")
    
    return {
        "error": error_type,
        "message": error_message
    }

def log_and_raise(error: Exception):
    """
    Log an error and re-raise it.

    Args:
        error (Exception): The exception to log and raise.

    Raises:
        Exception: The same exception that was passed in.
    """
    logger.error(f"Error occurred: {type(error).__name__} - {str(error)}")
    raise error

# Example usage
if __name__ == "__main__":
    try:
        raise CommandError("Invalid command received")
    except NebulaLinkError as e:
        error_details = handle_error(e)
        print(f"Handled error: {error_details}")

    try:
        log_and_raise(ConfigurationError("Missing required configuration"))
    except NebulaLinkError as e:
        print(f"Caught re-raised error: {type(e).__name__} - {str(e)}")