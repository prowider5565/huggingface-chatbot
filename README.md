# huggingface-chatbot

FastAPI service scaffold with Pydantic settings, SQLAlchemy, and Alembic.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

The health check is available at `GET /api/v1/health`.

## Database

Set `DATABASE_URL` in `.env`, then create and apply migrations:

```bash
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

SQLAlchemy models should inherit from `app.db.base.Base` and be imported from
`app/db/base.py` so Alembic can discover them.
