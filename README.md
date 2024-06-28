# NebulaLink Server

NebulaLink: Your cosmic bridge to remote PC mastery. Control your Windows 11 gaming rig from your Android device with voice-commanded AI, adaptive display management, and Nyrna-inspired program pausing. Seamlessly integrate with Moonlight for a stellar gaming experience, anywhere in the universe.

## Project Structure

The project follows a modular structure to ensure maintainability and scalability. For a detailed overview of the project structure, please refer to [STRUCTURE.md](STRUCTURE.md).

## Current Implementation Status

### Utils Package (`src/utils/`)

- **Logging Configuration** (`logging_config.py`): Configures logging for the application.
- **Error Handling** (`error_handling.py`): Provides custom exceptions and error handling utilities.

### Controllers (`src/controllers/`)

- **Power Controller** (`power_controller.py`): Manages system power operations (shutdown, restart, sleep, hibernate) and power plans.
- **Display Controller** (`display_controller.py`): Handles display settings, including resolution and refresh rate changes.
- **Program Controller** (`program_controller.py`): Manages running programs, including listing, pausing, and resuming.

### Server (`src/server/`)

- **NebulaLink Server** (`nebulalink_server.py`): Core server implementation using WebSockets for real-time communication.

### Main Application (`src/main.py`)

- Entry point for the NebulaLink Server application.

## Features

- Remote power control (shutdown, restart, sleep, hibernate)
- Power plan management
- Display settings control (resolution, refresh rate)
- Dummy display management
- Running program management (list, pause, resume)
- Real-time communication via WebSockets

## Usage

To start the NebulaLink Server:

```bash
python src/main.py
```

## Next Steps

- Implement comprehensive error handling and input validation
- Add authentication and security measures
- Create a configuration system for server settings
- Implement AI assistant for natural language command processing
- Integrate with Moonlight for game streaming
- Develop the Android client application

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See the [LICENSE.md](LICENSE.md) file for details.

## Disclaimer

This software is in early development and may not be suitable for production use. Use at your own risk.
