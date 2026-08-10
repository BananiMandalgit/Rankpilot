# RankPilot

RankPilot is an AI-powered website optimization platform for SEO and AEO work. This repository currently contains only the initial development foundation: the frontend shell, backend shell, crawler shell, AI shell, database structure, documentation scaffold, and local infrastructure for PostgreSQL and Redis.

## Purpose

The project will grow incrementally into a tool that can analyze websites, surface optimization opportunities, and eventually generate helpful recommendations. The initial stage intentionally avoids SEO analysis, AEO analysis, crawling logic, AI calls, authentication, reporting, or other product features.

## Technology Stack

- Frontend: React, TypeScript, Tailwind CSS, React Router, Axios, Recharts
- Backend: FastAPI, Pydantic, SQLAlchemy
- Database: PostgreSQL
- Infrastructure: Docker, Redis
- Crawler: Playwright, BeautifulSoup
- AI services: Gemini, Groq, Ollama placeholders for later integration

## Repository Structure

- `frontend/` - React application shell
- `backend/` - FastAPI application shell
- `crawler/` - crawler module skeleton
- `ai/` - AI service module skeleton
- `database/` - database structure placeholder
- `docs/` - project documentation scaffold
- `tests/` - test suite scaffold

## Local Development Setup

1. Clone the repository.
2. Copy the example environment files.
3. Start PostgreSQL and Redis with Docker.
4. Install frontend dependencies and run the React app.
5. Create a Python virtual environment, install backend dependencies, and run the API.

## Git Branch Workflow

- Do not work directly on `main`.
- Create feature branches such as `feature/frontend` or `feature/backend`.
- Keep changes small and focused.
- Open a pull request before merging.
- Ask for review before merging into `main`.

## Clone The Repository

```powershell
git clone <repository-url>
cd Rankpilot
```

## Environment Files

Copy the example files before starting local work:

```powershell
Copy-Item .env.example .env
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env
```

## Run The Frontend

```powershell
cd frontend
npm install
npm run dev
```

## Run The Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Start PostgreSQL And Redis

```powershell
docker compose up -d
```

## Verify The Foundation

- Open the frontend at `http://localhost:5173`.
- Check the backend health endpoint at `http://localhost:8000/api/v1/health`.
- Run the backend test with `pytest tests/backend/test_health.py`.

## Notes

- No application features are implemented yet.
- The repository is prepared for incremental development only.
