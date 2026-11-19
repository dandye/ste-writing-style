set dotenv-load := true

# Default environment file
env_file := ".env"

# Python resolution (prefer .venv / venv, fallback to python3)
export PYTHONPATH := "src:."
python := if path_exists(".venv/bin/python") == "true" { ".venv/bin/python" } else if path_exists("venv/bin/python") == "true" { "venv/bin/python" } else { "python3" }
has_uv := if `command -v uv >/dev/null 2>&1 && echo 1 || echo 0` == "1" { "true" } else { "false" }

# Default recipe: list available commands
default:
    @just --list

# ------------------------------------------------------------------------------
# Setup & Environment Management
# ------------------------------------------------------------------------------

# Setup local environment (.env, venv, and editable dependencies)
setup:
    #!/usr/bin/env bash
    set -e
    if [ ! -f "{{ env_file }}" ]; then
        echo "Creating {{ env_file }} from template..."
        cp .env.example "{{ env_file }}"
        echo "Created {{ env_file }}."
    fi
    if [ ! -d ".venv" ]; then
        if [ "{{ has_uv }}" = "true" ]; then
            echo "Creating virtualenv with uv..."
            uv venv .venv
        else
            echo "Creating virtualenv with python3..."
            python3 -m venv .venv
        fi
    fi
    just install

# Install or sync project dependencies
install:
    #!/usr/bin/env bash
    set -e
    if [ "{{ has_uv }}" = "true" ]; then
        echo "Installing editable dependencies via uv..."
        uv pip install -e ".[dev]"
    else
        echo "Installing editable dependencies via pip..."
        {{ python }} -m pip install --upgrade pip
        {{ python }} -m pip install -e ".[dev]"
    fi

# ------------------------------------------------------------------------------
# Quality & Testing
# ------------------------------------------------------------------------------

# Run unit tests with pytest
test *args="":
    {{ python }} -m pytest {{ args }}

# Run tests with coverage report
test-cov:
    {{ python }} -m pytest --cov=src --cov-report=term-missing --cov-report=html

# Lint code with ruff
lint:
    {{ python }} -m ruff check .
    {{ python }} -m ruff format --check .

# Format code and apply auto-fixes with ruff
format:
    {{ python }} -m ruff check --fix .
    {{ python }} -m ruff format .

# Typecheck source code with mypy
typecheck:
    {{ python }} -m mypy src

# ------------------------------------------------------------------------------
# Execution & STE CLI Commands
# ------------------------------------------------------------------------------

# Run project CLI (proxies to manage.py)
run *args="":
    {{ python }} manage.py {{ args }}

# Display environment and dictionary information
info:
    {{ python }} manage.py info

# Audit a markdown document for ASD-STE100 compliance
audit target:
    {{ python }} manage.py audit {{ target }}

# Generate or validate .ste-dictionary.yaml
dict-gen *args="":
    {{ python }} manage.py dict-gen {{ args }}

# Clean build artifacts, bytecode, and test caches
clean:
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov dist build *.egg-info
