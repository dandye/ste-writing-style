# Setup & Installation - ste-writing-style

## Prerequisites

- Python >= 3.11
- `just` (command runner)
- `uv` (recommended fast package installer) or `pip`

## Quick Start

1. Initialize environment and install dependencies:
   ```bash
   just setup
   ```
2. Run test suite:
   ```bash
   just test
   ```
3. Run linter and formatting:
   ```bash
   just lint
   just format
   ```
4. Audit a markdown file:
   ```bash
   python manage.py audit path/to/document.md
   ```
