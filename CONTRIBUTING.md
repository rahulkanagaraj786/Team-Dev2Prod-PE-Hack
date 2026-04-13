# Contributing Guide

Thank you for contributing to this project! This document covers how to set up your environment, run tests, and submit changes.

## Setup

1. Install [uv](https://github.com/astral-sh/uv):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Copy `.env.example` to `.env` and fill in your values.
4. Start the database and run migrations, then start the server:
   ```bash
   uv run python run.py
   ```

## Project Structure

```
app/
  models/     # Peewee ORM models (User, URL, Link, Event)
  routes/     # Flask Blueprints for each resource
  services/   # Business logic (URL creation, redirect resolution)
  errors.py   # Centralized JSON error handlers
  database.py # DB connection and table initialization
```

## Running Tests

```bash
uv run pytest
```

## Submitting a Pull Request

1. Branch off `main` with a descriptive name (`feature/...`, `fix/...`).
2. Keep commits focused — one logical change per commit.
3. Make sure `uv run pytest` passes before opening the PR.
4. Write a clear PR description explaining *what* and *why*.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Use type hints where practical.
- Keep route handlers thin — push logic into `services/`.
