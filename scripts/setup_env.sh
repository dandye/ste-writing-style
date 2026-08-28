#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

if command -v uv >/dev/null 2>&1; then
    echo "Using uv to configure virtual environment..."
    [ ! -d .venv ] && uv venv .venv
    uv pip install -e ".[dev]"
else
    echo "Using python3 -m venv to configure virtual environment..."
    [ ! -d .venv ] && python3 -m venv .venv
    ./.venv/bin/pip install --upgrade pip
    ./.venv/bin/pip install -e ".[dev]"
fi

echo "Environment setup complete."
