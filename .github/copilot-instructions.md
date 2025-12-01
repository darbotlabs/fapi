# FAPI Repository - Copilot Instructions

## Project Overview

FAPI is a fork and agentic continuation of FastAPI, managed by authoritative intelligence agents as part of the darbot framework. It is a high-performance Python web framework for building APIs with automatic interactive documentation.

## Prerequisites

- Python 3.8 or higher (tested with 3.12.3)
- Git
- Virtual environment recommended

## Setup and Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install FAPI with all dependencies
pip install -e ".[all]"

# Install development and testing dependencies
pip install -r requirements-tests.txt
```

## Build and Test Commands

### Linting

```bash
# Run all linting checks (mypy + ruff)
bash scripts/lint.sh

# Or run individually:
mypy fastapi
ruff check fastapi tests docs_src scripts
ruff format fastapi tests --check
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
bash scripts/test.sh

# Run specific test file
pytest tests/path/to/test_file.py -v

# Run tests with coverage report
pytest tests/ --cov=fastapi --cov-report=html
```

### Formatting

```bash
# Format code
ruff format fastapi tests
```

### Running the Development Server

```bash
# Start development server with auto-reload
fastapi dev main.py --port 8043

# Alternative using uvicorn directly
uvicorn main:app --reload --port 8043
```

## Project Structure

```text
fapi/
├── fastapi/              # Main FastAPI package source code
├── tests/                # Comprehensive test suite
├── docs/                 # Documentation (multiple languages)
├── docs_src/             # Documentation source code examples
├── scripts/              # Utility scripts (lint.sh, test.sh, format.sh)
├── starlette/            # Starlette vendored code
├── pyproject.toml        # Project configuration and dependencies
├── requirements*.txt     # Various dependency specifications
└── README.md             # Project documentation
```

## Code Style and Conventions

### Python Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Use Pydantic for data validation and settings management
- Follow the existing code style in the repository

### Linting Configuration

- **ruff**: Used for linting and formatting (configured in `pyproject.toml`)
- **mypy**: Used for static type checking with strict mode enabled
- Plugins: `pydantic.mypy` for Pydantic support

### Import Order

- Use isort-compatible import ordering (handled by ruff)
- Known third-party packages: `fastapi`, `pydantic`, `starlette`

### Naming Conventions

- Use snake_case for functions and variables
- Use PascalCase for classes
- Use UPPER_CASE for constants

## Testing Requirements

- All new features should have corresponding tests
- Tests are located in the `tests/` directory
- Use pytest for testing
- Maintain test coverage for the codebase
- Tests support both Pydantic v1 and Pydantic v2

## Dependencies

### Core Dependencies

- `starlette>=0.40.0,<0.51.0` - Web framework foundation
- `pydantic>=1.7.4,<3.0.0` - Data validation
- `typing-extensions>=4.8.0` - Type hint extensions
- `annotated-doc>=0.0.2` - Documentation utilities

### Development Dependencies

- `pytest` - Testing framework
- `coverage` - Code coverage
- `mypy` - Static type checking
- `ruff` - Linting and formatting
- `httpx` - HTTP client for testing

## Key Files

- `pyproject.toml` - Project configuration, dependencies, and tool settings
- `requirements-tests.txt` - Test dependencies
- `scripts/lint.sh` - Linting script
- `scripts/test.sh` - Test runner script
- `scripts/format.sh` - Code formatting script

## Important Notes

- FAPI maintains compatibility with both Pydantic v1 and v2
- The project uses PDM as the build backend
- Pre-commit hooks are configured for automated formatting and linting
- Always run linting before submitting changes: `bash scripts/lint.sh`
- Always run tests before submitting changes: `pytest tests/ -v`

## Boundaries and Exclusions

- Do not modify vendored code in `starlette/` unless specifically required
- Do not modify generated documentation files
- Keep changes minimal and focused on the specific task
- Preserve backward compatibility when possible
