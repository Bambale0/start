# ADR 0006 — Domain Events and Transactional Outbox

**Status:** Accepted

## Context

The platform will trigger asynchronous work, integrations, notifications, analytics and workflow reactions after business state changes.

Writing DB state and independently publishing messages risks partial failure.

## Decision

Material domain changes emit typed versioned events.

When an event must survive process failure and trigger asynchronous work, persist it transactionally with business state in an outbox.

A publisher forwards committed outbox records to the queue/event transport.

Consumers are idempotent.

## Consequences

Event envelopes need stable IDs, type, version, scope and correlation metadata.

Consumers must tolerate duplicate delivery.

Operational tooling must monitor outbox lag and failed consumers.
