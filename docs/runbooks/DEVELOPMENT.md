# Development Runbook

## Local setup

Python 3.12+ is required.

Commands:

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -e ".[dev]"
    cp .env.example .env
    make check
    make run

Or use Docker Compose:

    cp .env.example .env
    docker compose up --build

## Before changing code

1. Read AGENTS.md.
2. Read relevant architecture/spec/ADR files.
3. Inspect relevant code and tests.
4. Use the relevant Bambale0/skills flow.
5. Define acceptance criteria.
6. Identify tenant, authorization, migration, observability and integration impact.

## Required local checks

    ruff check .
    ruff format --check .
    mypy src
    pytest

## Adding a domain module

Before adding a module, answer:

- Is it universal or vertical-specific?
- Which tenant owns the data?
- Which permissions protect it?
- Which events does it emit?
- Which configuration is mutable?
- Which audit is required?
- Which tests prove tenant isolation?

## Adding an integration

Document:

- source of record;
- sync direction;
- authentication;
- secret storage;
- timeout;
- retry;
- rate limits;
- idempotency;
- webhook verification;
- reconciliation;
- data freshness;
- failure semantics;
- contract tests.

## Adding a workflow

Workflow definitions are data/configuration.

Do not introduce arbitrary admin-executed Python.

Version definitions and preserve the version used by running instances.

## Environment files

.env.example contains development examples only.

Never commit .env or production credentials.
