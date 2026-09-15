# ADR 0001 — Modular Monolith First

**Status:** Accepted

## Context

The product spans identity, workflows, cases, assets, documents, integrations, analytics and several industries.

The domain is still being learned through the first real customer deployment.

Premature microservices would increase deployment and consistency complexity while making cross-cutting changes expensive.

## Decision

Start as a modular monolith with strict module boundaries and explicit internal contracts.

Long-running/background work may run in separate worker processes while sharing the same versioned application code/domain contracts.

## Consequences

Positive:

- faster product learning;
- simpler transactions;
- easier refactoring;
- lower operational overhead;
- easier end-to-end tests.

Required discipline:

- no uncontrolled cross-module imports;
- no hidden direct writes into another module's tables;
- provider adapters stay at the edge;
- domain events are explicit.

A module may be extracted only with evidence of scale, reliability, security, release cadence or ownership need.
