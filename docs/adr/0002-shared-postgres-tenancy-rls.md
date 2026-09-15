# ADR 0002 — Shared PostgreSQL Tenancy with RLS

**Status:** Accepted

## Context

Organizations must be hard security boundaries while authorized owners need cross-company analytics.

Database-per-tenant would increase operational cost and complicate group aggregation during early product development.

Application-only tenant filtering is too fragile for a high-value multi-company system.

## Decision

Use a shared PostgreSQL database for the initial architecture.

Tenant-bound records carry explicit `organization_id`.

Use defense in depth:

- server-side membership resolution;
- typed tenant context;
- tenant-aware repositories;
- PostgreSQL Row Level Security for tenant-bound tables where practical;
- release-blocking tenant-isolation tests.

Group-level data uses explicit `group_id`.

## Consequences

Cross-company aggregation is efficient under authorized scope.

Every background worker/job must establish tenant context explicitly.

Unsafe raw SQL paths are security-sensitive.

Future regulated customers may use isolated database topology behind the same domain/repository contracts if required.
