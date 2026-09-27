# Development Workflow

Welcome to the JurisPulse development guide. This document outlines the general conventions and workflows we follow.

## Frontend vs Backend Separation

The repository is a monorepo separated cleanly into:
- `/frontend/`: React SPA running on Node.js/Vite.
- `/backend/`: FastAPI application running on Python 3.11+.

These two environments do not share dependencies and should be started in separate terminal windows. They communicate entirely over REST APIs (defaulting to `http://localhost:8000/api/v1` during local development).

## Environment Handling

We use `.env` files to manage secrets and environment-specific configuration. 
**Never commit `.env` files to version control.**

- Copy `.env.example` to `.env` in both the `frontend/` and `backend/` directories before starting development.
- The backend relies heavily on environment variables for Supabase connections, database strings, and secret keys. The application will fail to start if critical variables are missing.

## Directory Conventions

- **Frontend Features**: The frontend uses a feature-sliced architecture (`src/features/`). Keep business logic for a specific domain (e.g., `cases`, `documents`) isolated within its feature directory. Use `src/components/` only for highly reusable, generic UI components.
- **Backend Modules**: The backend follows Domain-Driven Design (DDD). Each domain (e.g., `auth`, `cases`) lives in `backend/app/modules/`. Try to keep cross-module dependencies to a minimum.

## Database Migrations

Always generate Alembic migrations when changing SQLAlchemy models:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Tooling and Formatting

- **Frontend**: We use `oxlint` for linting and Tailwind for styling.
- **Backend**: We use `black` and `ruff` for formatting and linting, and `mypy` for static type checking. Ensure you run these tools before pushing code.
