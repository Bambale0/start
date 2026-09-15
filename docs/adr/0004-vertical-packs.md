# ADR 0004 — Vertical Packs Instead of Separate CRM Codebases

**Status:** Accepted

## Context

The target customer group can operate unrelated businesses such as property management, construction and fleet/service.

Building a custom CRM codebase for each would repeat identity, permissions, workflow, documents, integrations and analytics.

## Decision

Use one universal core plus versioned Vertical Packs.

A pack may define:

- object/asset/case/work-order types;
- forms;
- terminology;
- workflows;
- SLA templates;
- dashboards;
- domain validation extensions.

A pack does not own separate authentication, authorization, workflow runtime, integration secret management or audit.

## Consequences

A new vertical should be mostly configuration and bounded extensions.

If a new domain requires copying a core service, architecture review is required.
