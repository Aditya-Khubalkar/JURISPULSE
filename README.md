# JurisPulse

### Legal intelligence, in motion.

JurisPulse is a legal workflow platform built for the Indian legal ecosystem. It connects case management, physical document processing, and AI-assisted research into a single, cohesive interface.

**React** · **TypeScript** · **FastAPI** · **PostgreSQL** · **Celery** · **Redis**

[Architecture](./PROJECT_STRUCTURE.md) | [Documentation](./docs/development/)

---

## The Vision

JurisPulse is designed to solve a fundamental problem in Indian legal practice: fragmentation. Client communication, physical document parsing, and legal research typically occur across disconnected tools. 

JurisPulse brings these workflows into a unified, programmable environment.

### Product Overview

| Module | Purpose |
| --- | --- |
| **Case Intelligence** | Client management, case timelines, and automated hearing tracking. |
| **Document Intelligence** | Tesseract OCR ingestion, layout parsing, and semantic chunking. |
| **Legal Research** | pgvector-backed semantic search across historical case laws. |
| **AI Workflows** | LLM-assisted drafting and hallucination verification services. |

## Project Status

**Active development**

JurisPulse is currently in its initial structural phase. The core architecture is established, but feature implementation is ongoing.

### Current Implementation

- **Project Scaffold**: Monorepo structure properly segregating frontend and backend logic.
- **Database Architecture**: SQLAlchemy models for core domains (users, organizations, cases, documents) and Alembic migrations.
- **API Foundation**: Defined API routing structure grouped by domain modules.
- **Frontend Design System**: React application initialized with Vite, Tailwind CSS tokens, and a Zustand state store.

### Planned Capabilities

The following subsystems are designed and pending implementation:

- **Client & Case Timelines**: End-to-end case tracking and automated reminders.
- **OCR Ingestion Pipeline**: Processing physical documents via Tesseract and storing semantic chunks.
- **AI-Assisted Drafting**: Generating legal text securely using fine-tuned models.
- **Hallucination Detection**: Built-in verification cross-referencing AI output with established case laws.

## Architecture

```mermaid
flowchart LR
    Client[Web Client] --> Frontend[React SPA]
    Frontend --> API[FastAPI]
    
    API --> DB[(PostgreSQL)]
    API -.-> Redis[(Redis)]
    Redis -.-> Workers[Celery]
    Workers --> DB
```

The system is separated into three core domains:
- **Frontend Layer**: A React SPA handling UI state and data fetching.
- **API Layer**: A FastAPI application mapping business logic to specific REST endpoints.
- **Asynchronous Layer**: Celery workers polling Redis for heavy tasks like OCR.

## Tech Stack

- **Frontend**: React (19), TypeScript (6.0), Vite (8.2), Tailwind CSS (4.3), Zustand, React Router, React Query.
- **Backend**: Python (3.11+), FastAPI, SQLAlchemy, Alembic, Celery, Redis, Structlog.
- **Database**: PostgreSQL (via Supabase / async psycopg), pgvector.
- **Infrastructure**: Docker Compose.

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

## Getting Started

### 1. Environment Configuration

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
Configure the variables for your local or Supabase database before proceeding.

### 2. Backend API Setup

Requires Python 3.11+.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```

*Note: Database migrations (`alembic upgrade head`) and Celery workers are configured but may require additional local setup of PostgreSQL/Redis.*

### 3. Frontend Setup

Requires Node.js.

```bash
cd frontend
npm install
npm run dev
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
