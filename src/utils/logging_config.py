# src/utils/logging_config.py

import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional

def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with console and optionally file output.

    Args:
        name (str): Name of the logger.
        log_file (Optional[str]): Path to the log file. If None, only console logging is set up.
        level (int): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is provided
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with the given name.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Logger instance.
    """
    return logging.getLogger(name)

# Example usage
if __name__ == "__main__":
    # Set up the main logger
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    main_logger = setup_logger("nebulalink", os.path.join(log_directory, "nebulalink.log"))

    # Example log messages
    main_logger.debug("This is a debug message")
    main_logger.info("This is an info message")
    main_logger.warning("This is a warning message")
    main_logger.error("This is an error message")
    main_logger.critical("This is a critical message")

    # Get a logger for a specific module
    module_logger = get_logger("nebulalink.server")
    module_logger.info("This is a log message from a specific module")