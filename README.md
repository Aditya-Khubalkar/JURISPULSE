<div align="center">

  <h1>⚖️ JurisPulse</h1>

  <img src="https://readme-typing-svg.herokuapp.com?font=Inter&weight=600&size=24&pause=1000&color=3B82F6&center=true&vCenter=true&width=600&lines=Legal+intelligence,+in+motion.;Unified+case+management.;AI-assisted+legal+research.;Physical+document+parsing." alt="Typing SVG" />

  <p>
    <b>JurisPulse is a legal workflow platform built for the Indian legal ecosystem.</b><br/>
    It connects case management, physical document processing, and AI-assisted research into a single, cohesive interface.
  </p>

  <p>
    <a href="https://react.dev/"><img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react" alt="React" /></a>
    <a href="https://www.typescriptlang.org/"><img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" /></a>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /></a>
    <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" /></a>
    <a href="https://redis.io/"><img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" /></a>
    <a href="https://docs.celeryq.dev/"><img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery" /></a>
  </p>

  <p>
    <a href="./PROJECT_STRUCTURE.md"><b>Architecture</b></a> •
    <a href="./docs/development/"><b>Documentation</b></a>
  </p>

</div>

---

## 📖 The Vision

JurisPulse is designed to solve a fundamental problem in Indian legal practice: fragmentation. Client communication, physical document parsing, and legal research typically occur across disconnected tools. 

JurisPulse brings these workflows into a unified, programmable environment.

### 🚀 Product Overview

| Module | Purpose |
| --- | --- |
| **Case Intelligence** | Client management, case timelines, and automated hearing tracking. |
| **Document Intelligence** | Tesseract OCR ingestion, layout parsing, and semantic chunking. |
| **Legal Research** | pgvector-backed semantic search across historical case laws. |
| **AI Workflows** | LLM-assisted drafting and hallucination verification services. |

## 🚧 Project Status

Active development

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

## 🏗️ Architecture

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

## 💻 Technology

| Layer | Core Technologies |
|---|---|
| **Frontend** | React 19, TypeScript 6, Vite 8, Tailwind CSS |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy, Alembic |
| **Database** | PostgreSQL (Supabase / asyncpg), pgvector |
| **Async Workers** | Celery, Redis |

## 📂 Repository

```text
JurisPulse/
├── frontend/           # React SPA
├── backend/            # FastAPI application
├── infrastructure/     # Planned: Docker, Nginx, deployment
├── docs/               # System documentation
├── scripts/            # Planned: Utility scripts
├── tests/              # Planned: Test suites
└── .github/            # GitHub metadata
```

For a detailed breakdown of the internal architecture, see [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md).

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v18+)
- **Python** (3.11+)
- **PostgreSQL** (Local or Supabase)

### 1. Environment
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
Update `.env` files with your database credentials.

### 2. Backend API
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run migrations and start server
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend SPA
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Architecture](./PROJECT_STRUCTURE.md) | High-level system architecture and repository map. |
| [Development Workflow](./docs/development/WORKFLOW.md) | Guidelines for local setup, branching, and testing. |

## 📄 License

This project is proprietary and confidential. All rights reserved.
