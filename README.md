# NebulaLink Server

NebulaLink: Your cosmic bridge to remote PC mastery. Control your Windows 11 gaming rig from your Android device with voice-commanded AI, adaptive display management, and Nyrna-inspired program pausing. Seamlessly integrate with Moonlight for a stellar gaming experience, anywhere in the universe.

## Project Structure

The project follows a modular structure to ensure maintainability and scalability. For a detailed overview of the project structure, please refer to [STRUCTURE.md](STRUCTURE.md).

## Current Implementation Status

### Utils Package (`src/utils/`)

The `utils` package contains utility modules that provide foundational functionality for the NebulaLink server. Currently implemented:

1. **Logging Configuration** (`logging_config.py`):

   - `setup_logger()`: Configures a logger with console and optional file output.
   - `get_logger()`: Retrieves a logger for different parts of the application.

2. **Error Handling** (`error_handling.py`):

   - Custom exception classes (e.g., `NebulaLinkError`, `CommandError`, `PowerControlError`).
   - `handle_error()`: Standardized error handling and logging.
   - `log_and_raise()`: Logs an error before re-raising it.

3. **Package Initialization** (`__init__.py`):
   - Exposes key functions and classes from the utils package for easy importing.

## Usage

To use the utility functions in your code:

```python
from utils import get_logger, CommandError, handle_error

logger = get_logger(__name__)

try:
    # Your code here
    raise CommandError("Example error")
except CommandError as e:
    error_details = handle_error(e)
    logger.error(f"Command error occurred: {error_details}")
```

## Next Steps

- Implement core server functionality in `src/server/nebulalink_server.py`
- Develop controller modules for power, display, and program management
- Set up the main application entry point in `src/main.py`

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See the [LICENSE.md](LICENSE.md) file for details.
