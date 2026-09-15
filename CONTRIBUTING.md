# Contributing

## Read first

All contributors and coding agents must follow:

- AGENTS.md;
- relevant docs under docs/;
- accepted ADRs.

Bambale0/skills is the primary engineering playbook for development work.

## Change shape

Prefer one coherent vertical slice per pull request.

A PR should explain:

- business/user outcome;
- architecture impact;
- data/migration impact;
- authorization and tenant impact;
- observability;
- tests;
- rollout risk.

## Required checks

Before proposing merge:

    ruff check .
    ruff format --check .
    mypy src
    pytest

Run additional integration/e2e/migration checks when relevant.

## Architecture changes

Create or supersede an ADR for changes to:

- tenancy;
- identity;
- authorization;
- system-of-record boundaries;
- core vs vertical boundary;
- workflow semantics;
- event envelope;
- service decomposition;
- high-impact AI authority.

## Business configuration

Do not add mutable business rules as source constants.

Expose appropriate configuration through the platform control plane.

## Secrets/data

Do not commit real credentials, customer exports, production dumps or real personal data.
