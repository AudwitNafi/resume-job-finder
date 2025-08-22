# resume-job-finder — README

A tool that parses resumes, analyzes job requirements, and matches candidates to relevant job postings. It automates job discovery by filtering, tracking, and suggesting best-fit opportunities.

---

## Quick summary

`resume-job-finder` is a modular FastAPI backend service that ingests resumes, extracts structured data, compares candidate profiles to job descriptions, and ranks matches. The project follows a production-friendly layout (clear separation of api, models, schemas, services, migrations, infra) and is designed for testability, CI, containerization, and team collaboration.

---

## Contents

* Features
* Architecture & folder layout
* Prerequisites
* Project setup (pyenv + `uv`)
* Development (run, test, lint)
* Deployment notes (Docker & migrations)
* Contributing
* License

---

## Features

* Resume parsing (PDF/DOCX -> structured fields)
* Job requirement analysis and matching algorithm
* CRUD for candidates and job postings
* Token-based authentication (JWT)
* Async DB (Postgres recommended), Alembic migrations
* Tests (pytest + httpx) and pre-commit-ready linting

---

## Architecture & final folder layout (what we will create)

All backend source and infra live under `backend/`. Root-level repository artifacts remain in project root.

```
RESUME-JOB-FINDER/
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
├── pyproject.toml
├── backend/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Makefile
│   ├── .env
│   ├── .env.example
│   ├── alembic/
│   ├── migrations/
│   ├── scripts/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── security.py
│       ├── api/
│       │   ├── deps.py
│       │   └── v1/
│       │       ├── api.py
│       │       └── endpoints/
│       │           ├── health.py
│       │           ├── auth.py
│       │           └── users.py
│       ├── db/
│       │   ├── base.py
│       │   └── session.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── user.py
│       ├── schemas/
│       │   └── user.py
│       ├── crud/
│       │   └── user.py
│       ├── services/
│       │   └── auth_service.py
│       ├── utils/
│       │   └── hashing.py
│       └── tests/
│           ├── conftest.py
│           └── test_users.py
```

---

## Prerequisites

* macOS / Linux / Windows (WSL recommended)
* `pyenv` installed and configured (to manage multiple Python versions)
* `uv` package manager (Ultrafast) installed
* Git
* Docker & docker-compose (for container/local stack; optional for dev)

> Recommended Python version: `3.10.x` or `3.11.x`. This README uses `3.10.2` as example because you already have it.

---

## Full, copyable setup — create directories, move files, and initialize with `uv`

> This single shell block:
>
> * creates the backend directory tree (no duplicates),
> * touches the placeholder files,
> * moves the `main.py` you currently have at repo root into `backend/app/main.py`,
> * sets the `pyenv` local version (example `3.10.2`),
> * creates a uv-managed venv using that interpreter,
> * adds recommended dependencies to the project,
> * installs them (sync),
> * shows commands to run the dev server.

Copy-paste and run from your project root (`RESUME-JOB-FINDER`):

```bash

# 1) Move your existing root main.py (if present) into the backend app (overwrite safe)
if [ -f main.py ]; then
  mv -f main.py backend/app/main.py
fi

# 3) Set the pyenv local interpreter (example: 3.10.2)
pyenv local 3.10.2

# 4) Create uv venv using the pyenv-picked python interpreter
uv venv --python "$(pyenv which python)"

# 5) Add recommended dependencies (or edit pyproject.toml manually)
uv add fastapi "uvicorn[standard]" sqlalchemy asyncpg pydantic python-dotenv alembic \
  pytest httpx pytest-asyncio black ruff isort

# 6) Install/sync dependencies
uv sync

# 7) Run dev server (two options)
# Option A (recommended): run inside uv-managed environment
uv run -- uvicorn backend.app.main:app --reload --port 8000

# Option B: activate venv then use python -m uvicorn
# source .venv/bin/activate
# python -m uvicorn backend.app.main:app --reload --port 8000
```

> Notes:
>
> * `uv add` appends dependencies to the project config; `uv sync` installs them.
> * If `uv run -- uvicorn ...` fails, use Option B (activate venv).

---

## Example `.env.example`

Create `backend/.env.example` with these keys (do not commit real secrets):

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/resume_job_finder
SECRET_KEY=replace-with-a-secure-random-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

Copy to `.env` and fill values before running in dev or CI.

---

## Common operations

* Start dev server

  ```bash
  uv run -- uvicorn backend.app.main:app --reload --port 8000
  ```

  or activate venv and:

  ```bash
  source .venv/bin/activate
  python -m uvicorn backend.app.main:app --reload --port 8000
  ```

* Run tests

  ```bash
  uv run -- pytest -q
  ```

  or with activated venv:

  ```bash
  pytest -q
  ```

* Create an Alembic migration (after editing models)

  ```bash
  uv run -- alembic revision --autogenerate -m "describe change"
  uv run -- alembic upgrade head
  ```

* Lint & format

  ```bash
  uv run -- ruff check .
  uv run -- black .
  uv run -- isort .
  ```

---

## Docker & docker-compose (quick note)

* `backend/Dockerfile` should build with a slim Python image, copy source, install deps, and run `uvicorn backend.app.main:app`.
* `backend/docker-compose.yml` can include `db` (Postgres) and `web` services plus a volume for migrations.

I can produce a production-ready `Dockerfile` + `docker-compose.yml` if you want.

---

## Tests & CI

* Use pytest and `httpx.AsyncClient` for API tests. Keep test DB in `pytest` fixtures (separate `DATABASE_URL`).
* Recommend GitHub Actions to run linters + tests and build the Docker image on push to `main`.

---

Got it 👍 — here’s a clean **README section with only Alembic steps** that you can drop in:

---

## 📦 Database Migrations (Alembic)

We use [Alembic](https://alembic.sqlalchemy.org/) for database migrations.

### Running Migrations

* **Apply all migrations to the database**

  ```bash
  alembic upgrade head
  ```

* **Revert the last migration**

  ```bash
  alembic downgrade -1
  ```

### Creating New Migrations

* **Autogenerate a new migration** based on model changes:

  ```bash
  alembic revision --autogenerate -m "description_of_change"
  ```

* **Create an empty migration** (manual SQL):

  ```bash
  alembic revision -m "manual_migration"
  ```

### Checking Current DB Version

```bash
alembic current
```

### Viewing Migration History

```bash
alembic history --verbose
```

---

## Next steps I can do for you (pick one)

1. Generate real starter content for each touched file (skeleton code for all files created above).
2. Produce a `Dockerfile` + `docker-compose.yml` tailored to Postgres + Redis + worker.
3. Create GitHub Actions CI YAML (lint, test, build).
4. Create a minimal working `backend/app/main.py` + one working endpoint (`/api/v1/health`) so you can `uv run` immediately.

Tell me which one and I’ll scaffold the code now.
