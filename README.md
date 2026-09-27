# JurisPulse

JurisPulse is a multi-agent legal workflow orchestration platform designed for legal professionals. It provides advanced case management, document processing, legal research, AI-assisted drafting, and hallucination detection for legal documents.

## Features

- **Case Management**: End-to-end case tracking, client management, and timeline visualization.
- **Document Processing**: OCR-enabled document ingestion with local and cloud storage support.
- **Legal Research**: AI-powered vector search over legal databases for precedents and case laws.
- **AI-Assisted Drafting**: Automated drafting of legal documents using fine-tuned language models.
- **Hallucination Detection**: Built-in verification steps to ensure AI-generated legal text is factually accurate.
- **Collaboration**: Secure team collaboration, notifications, and task management.

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

1. Create a virtual environments and install dependencies:
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
