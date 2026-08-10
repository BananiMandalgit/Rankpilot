# RankPilot - Copilot Instructions

## Project Overview

RankPilot is an AI-powered website optimization platform for
Search Engine Optimization (SEO) and Answer Engine Optimization (AEO).

The platform will eventually:

- Crawl publicly accessible websites
- Perform SEO analysis
- Perform AEO analysis
- Analyze website content
- Extract relevant keywords and topics
- Generate AI-powered recommendations
- Rewrite selected content
- Generate FAQs
- Generate JSON-LD Schema markup
- Perform limited competitor analysis
- Generate SEO/AEO reports

IMPORTANT:
The project will be developed incrementally.
Do not implement the entire system at once.

---

## Technology Stack

### Frontend

- React
- TypeScript
- Tailwind CSS
- React Router
- Axios
- Recharts

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy

### Database

- PostgreSQL

### Infrastructure

- Docker
- Redis

### Background Processing

- Celery may be introduced later when asynchronous/background
  processing is actually required.

### AI

- Gemini API
- Groq as an optional cloud inference provider
- Ollama as an optional local development provider

### NLP

- spaCy
- TextStat
- Sentence Transformers may be introduced later if semantic
  similarity functionality requires it.
- scikit-learn may be introduced later if an actual ML component
  requires it.

### Crawler

Initial crawler stack:

- Playwright
- BeautifulSoup

Scrapy may be introduced later only if advanced crawling
requirements justify it.

### Reports

- ReportLab
- OpenPyXL

### Development

- Git
- GitHub
- GitHub Copilot
- VS Code

---

## Architecture Rules

- Keep frontend and backend separate.
- Keep crawler, SEO, AEO and AI modules separate.
- Do not put business logic inside React components.
- Do not put business logic directly inside FastAPI route handlers.
- Use service layers in the backend.
- Use Pydantic schemas for API request/response validation.
- Keep database models separate from API schemas.
- Use environment variables for configuration and secrets.
- Never commit API keys, passwords or secrets.
- Never commit .env files.
- Use .env.example for required environment variables.
- Keep modules loosely coupled.
- Prefer simple and maintainable architecture.
- Avoid unnecessary microservices.

---

## Project Module Structure

The project will use the following major modules:

- frontend/ → React user interface and dashboard
- backend/ → FastAPI application and API layer
- crawler/ → Website crawling and page data extraction
- ai/ → LLM integration and AI services
- database/ → Database configuration, migrations and models
- docs/ → Architecture and project documentation
- tests/ → Unit and integration tests

---

## SEO Architecture

SEO analysis should primarily use deterministic,
rule-based checks.

Examples:

- Page title
- Meta description
- Heading structure
- Image ALT text
- Internal links
- External links
- Broken links
- Canonical URL
- Robots directives
- Sitemap
- HTTPS
- Structured data
- Basic content metrics

Do not use an LLM for simple deterministic checks.

---

## AEO Architecture

AEO will use a transparent, heuristic-based evaluation framework.

Potential dimensions include:

- Question coverage
- Q&A structure
- FAQ quality
- Content structure
- Readability
- Entity/topic coverage
- Answer completeness
- Structured data

The AEO score is a project-defined metric.

Do not present it as an official industry-standard score.

The final scoring methodology and weights must be documented
and justified by the project team.

---

## AI Architecture Rules

Use LLMs for tasks where language understanding or generation
provides real value.

Examples:

- Explaining detected issues
- Generating recommendations
- Rewriting content
- Generating FAQs
- Generating metadata
- Generating Schema markup
- Summarizing reports

Do NOT use an LLM unnecessarily for deterministic checks.

Example:

Bad approach:

Ask an LLM whether a title contains more than 60 characters.

Good approach:

Use Python to count the characters.

Keep AI provider integrations inside the AI service layer.

Do not call Gemini, Groq or Ollama directly from frontend components.

Prompts should be kept modular and maintainable.

LLM-generated output must be validated before being stored
or displayed when structured output is expected.

Never assume that an LLM response is automatically correct.

---

## Security Rules

- Never expose API keys in frontend code.
- Never hardcode API keys.
- Never commit .env files.
- Never hardcode database passwords.
- Validate user-supplied URLs.
- Restrict crawler operations to appropriate domains.
- Implement crawl limits and timeouts.
- Do not allow unrestricted server-side URL fetching.
- Sanitize external content before displaying it.
- Validate all external input.

---

## Crawler Rules

The initial crawler should focus on publicly accessible websites.

The crawler must:

- Respect configured crawl limits.
- Avoid duplicate URLs.
- Normalize URLs.
- Handle HTTP errors.
- Handle timeouts.
- Avoid infinite crawling.
- Keep crawler logic separate from SEO/AEO analysis.

Do not implement advanced crawling features unless required.

---

## Git Rules

- Never work directly on main.
- Always use feature branches.
- Keep commits small and meaningful.
- Do not modify unrelated files.
- Do not rewrite another developer's implementation unnecessarily.
- Pull the latest main before starting new feature work.
- Create a Pull Request before merging into main.
- At least one teammate should review a Pull Request.
- Never force-push to main.

Recommended branch naming:

feature/crawler
feature/seo-engine
feature/aeo-engine
feature/ai-service
feature/frontend
feature/backend

---

## Coding Rules

- Prefer clean and readable code.
- Use meaningful variable and function names.
- Add type hints to Python code.
- Prefer TypeScript types/interfaces over any.
- Handle errors explicitly.
- Validate external input.
- Avoid unnecessary dependencies.
- Write tests for important business logic.
- Keep functions reasonably small.
- Avoid duplicated logic.
- Follow the existing project architecture.
- Do not introduce a new framework without justification.

---

## Simplicity Rule

RankPilot is a final-year B.Tech CSE project developed by
a six-member student team.

Prefer:

- Simple solutions
- Modular architecture
- Readable code
- Minimal dependencies
- Well-tested components
- Easy local development

Do NOT introduce the following unless there is a clear requirement:

- Microservices
- Kubernetes
- Kafka
- Complex agent frameworks
- Unnecessary vector databases
- Distributed systems
- Other enterprise-level infrastructure

Use the simplest technology that satisfies the current requirement.

Do not introduce a technology merely because it is listed as optional.

---

## Development Workflow

For non-trivial changes:

1. Understand the existing architecture.
2. Identify affected files.
3. Briefly state the planned changes.
4. Implement the smallest complete change.
5. Run relevant tests.
6. Review changes for unintended modifications.
7. Report what was changed and any remaining issues.

For simple edits, avoid unnecessary explanations or changes.

---

## Important Development Restriction

Do not implement the entire RankPilot application in one step.

Build the project incrementally.

Before implementing major features, ensure that the
existing foundation is working correctly.

Do not implement SEO, AEO, AI recommendations, advanced crawling,
authentication, competitor analysis or reporting during the
initial project-foundation stage unless explicitly requested.
