# Work Effort Manager Installation Guide

## Prerequisites
- Python 3.8 or higher

## Quick Start
```bash
# 1. Clone and enter directory
git clone <repository-url>
cd novabrew/work_effort_manager

# 2. Install dependencies
pip install poetry
poetry install

# 3. Run
poetry run unpack
```

## Development
```bash
# Format code
poetry run black .

# Run tests
poetry run pytest
```

## Troubleshooting
- If Poetry isn't found in your PATH after installation, restart your terminal
- If you get permission errors, try running the commands with sudo (Linux/macOS)
- For Windows users, you might need to run PowerShell as administrator

## Development Setup

To set up for development: