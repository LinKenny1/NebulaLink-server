# NebulaLink Server Repository Structure

This document outlines the directory structure and file organization for the NebulaLink Server project. Use this as a reference when navigating the project or adding new components.

```
nebulalink-server/
│
├── src/
│   ├── __init__.py
│   ├── main.py                  # Entry point of the application
│   │
│   ├── server/
│   │   ├── __init__.py
│   │   └── nebulalink_server.py # Core server implementation
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── power_controller.py  # Handles power-related operations
│   │   ├── display_controller.py # Manages display settings
│   │   └── program_controller.py # Controls program pausing/resuming
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging_config.py    # Logging configuration
│   │   └── error_handling.py    # Custom error handling utilities
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py          # Application-wide settings
│
├── tests/
│   ├── __init__.py
│   ├── test_server.py           # Tests for the main server
│   ├── test_power_controller.py
│   ├── test_display_controller.py
│   └── test_program_controller.py
│
├── docs/
│   ├── README.md                # General documentation
│   ├── CONTRIBUTING.md          # Contribution guidelines
│   ├── API.md                   # API documentation
│   └── CHANGELOG.md             # Version history and changes
│
├── scripts/
│   └── install_service.py       # Script to install as Windows service
│
├── .gitignore                   # Specifies intentionally untracked files
├── requirements.txt             # Project dependencies
├── setup.py                     # Package and distribution management
├── pyproject.toml               # Project configuration (for tools like Black)
└── README.md                    # Project overview and quick start guide
```

## Directory Descriptions

1. `src/`: Contains the main source code for the application.

   - `main.py` is the entry point of the application.
   - `server/` contains the core server implementation.
   - `controllers/` houses modules for different functionalities.
   - `utils/` includes utility functions and helpers.
   - `config/` stores configuration files and settings.

2. `tests/`: Contains all test files, mirroring the structure of `src/`.

3. `docs/`: Holds project documentation.

4. `scripts/`: Contains utility scripts, such as for installing the server as a Windows service.

5. Root-level files are used for project configuration and information.

## Best Practices

1. Keep related functionality together in the appropriate controller.
2. Use meaningful names for modules, classes, and functions.
3. Maintain test coverage for all new functionality.
4. Update documentation when adding or changing features.
5. Use type hints and docstrings throughout the codebase.

## Adding New Features

When adding new features:

1. Create appropriate modules in the relevant directories (e.g., new controllers in `src/controllers/`).
2. Add corresponding test files in the `tests/` directory.
3. Update documentation as necessary, especially `API.md` for new endpoints or functionality.
4. Modify `main.py` if the new feature needs to be initialized with the server.

Remember to keep the project structure clean and organized as it grows. If new categories of functionality emerge, consider creating new directories to house them.
