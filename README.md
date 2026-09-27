# JurisPulse

JurisPulse is a legal workflow platform built for Indian legal professionals. It connects case management, document processing, and legal research into a single unified system.

## What it is

JurisPulse aims to streamline legal workflows by organizing client cases, integrating OCR for physical documents, and providing a foundation for AI-assisted research and drafting. Currently, the repository contains the initial application scaffolding, the frontend design system, and the core database schema.

## Current capabilities

- **Project Scaffold**: Monorepo structure with React frontend and FastAPI backend.
- **Database Schema**: SQLAlchemy models for cases, users, organizations, documents, and roles.
- **API Routing**: Defined API endpoints grouped by domain modules.
- **Frontend Shell**: React application initialized with Vite, Tailwind CSS, and a Zustand store.

## Planned Features

- **Case Management**: Client management and timeline tracking.
- **Document Processing**: OCR-enabled document ingestion.
- **Legal Research**: Vector search over legal databases.
- **AI-Assisted Drafting**: LLM-powered drafting tools.
- **Verification**: Hallucination detection for legal text.

## Architecture

JurisPulse follows a modern, scalable client-server architecture:

- **Frontend**: A highly responsive Single Page Application (SPA) built with React, TypeScript, and Vite.
- **Backend**: A high-performance REST API built with FastAPI, using asynchronous database drivers.
- **Database**: PostgreSQL (with pgvector for semantic search) managed via SQLAlchemy and Alembic.
- **Workers**: Celery workers backed by Redis for asynchronous document processing and AI tasks.
- **AI Gateway**: Dedicated microservices for OCR, drafting, and embedding generation, abstracted behind internal services.

## Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Zustand, React Router, React Query.
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Alembic, Celery, Redis, Structlog.
- **Database**: PostgreSQL, Supabase, pgvector.
- **Infrastructure**: Docker, Nginx.

## Repository Structure

The repository is structured as a monorepo for maximum maintainability:

```text
JurisPulse/
├── frontend/           # React SPA and design system
├── backend/            # FastAPI application and AI integrations
├── infrastructure/     # Docker, Nginx, and deployment configurations
├── docs/               # Architecture, API, and development documentation
├── scripts/            # Utility scripts for database and deployment
├── tests/              # E2E and integration tests
└── .github/            # CI/CD workflows and issue templates
```

For a detailed breakdown of the internal architecture, see [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md).

## Local Development

### Environment Setup

1. Copy the example environment files:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```
2. Update the `.env` files with your local configuration (e.g., Supabase URLs, database credentials).

### Database Setup

Ensure PostgreSQL is running locally or use Supabase.
Run the database migrations:
```bash
cd backend
alembic upgrade head
```

### Backend Setup

1. Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
3. Start the Celery worker (in a separate terminal):
   ```bash
   celery -A app.workers.celery_app worker --loglevel=info
   ```

### Frontend Setup

1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Vite development server:
   ```bash
   npm run dev
   ```

### Docker Setup

You can run the entire stack using Docker Compose:
```bash
docker-compose up --build
```

## Testing

Run tests across the stack to ensure everything is working:

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
npm run test --prefix frontend
```

## Contribution Guidelines

We welcome contributions! Please review our `docs/development` guides for coding standards and branching strategies. Open an issue to discuss major architectural changes before submitting a pull request.

## License

This project is proprietary and confidential. All rights reserved.
