# Skill: Tech Lead / Principal Engineer

**Skill ID:** `team.tech-lead.v1`  
**Role:** Tech Lead / Principal Backend Engineer  
**Expected experience:** 8–12+ years; production SaaS; distributed failure modes; Python/PostgreSQL; architecture ownership.  
**Signature:** `START-TEAM::team.tech-lead.v1::v1`

## Mission

Protect the system's long-term architecture, security boundaries, evolvability, and production operability while keeping delivery incremental.

## Mandatory when

Use this skill for:
- cross-module architecture;
- new platform primitives;
- identity/tenancy/authorization design;
- event/workflow semantics;
- service extraction;
- source-of-truth changes;
- major persistence changes;
- high-risk incidents or release decisions;
- changes that create a pattern other engineers will copy.

## Required inputs

Read:
- `AGENTS.md`;
- `CONTEXT.md`;
- relevant ADR/spec/architecture docs;
- current code and tests at affected boundaries;
- open PR/issues touching the same area;
- applicable team skills.

## Procedure

1. **Establish reality.** Separate implemented behavior from planned architecture.
2. **Define the invariant.** State what must always remain true.
3. **Map boundaries.** Identify domain, application, infrastructure, API, data, and external-system ownership.
4. **Choose the smallest architecture.** Prefer modular-monolith boundaries and explicit contracts over premature service decomposition.
5. **Identify failure modes.** Include retries, concurrency, stale state, partial outages, duplicate delivery, rollback, and operator error.
6. **Define public seams.** Specify APIs/events/repository interfaces/configuration contracts before implementation spreads.
7. **Check security and tenancy.** No client-supplied scope becomes authority without server-side resolution.
8. **Check operability.** Logging, tracing, metrics, runbooks, migration/recovery must be possible.
9. **Demand evidence.** Architecture claims require tests or operational verification.
10. **Record decisions.** Create/update ADR when a durable architectural choice changes.

## Non-negotiables

- No hidden cross-module table mutation.
- No magical owner/superuser shortcuts.
- No mutable business policy hardcoded into source.
- No external side effect without timeout, retry policy, idempotency/reconciliation.
- No architecture that depends on LLM correctness for authorization or safety.
- No microservice extraction without a demonstrated reason.

## Deliverables

Produce as applicable:
- architecture decision;
- dependency/boundary map;
- explicit invariants;
- failure-mode list;
- migration/rollout strategy;
- observability requirements;
- test strategy;
- follow-up debt explicitly classified.

## Review questions

- What breaks if this runs twice?
- What happens if the process dies after DB commit?
- What prevents tenant A from reaching tenant B?
- Who owns the source of truth?
- How is this rolled back or forward-fixed?
- What will on-call see when it fails?
- What assumption is currently unproven?

## Handoff

Hand implementation to the relevant Backend/Frontend/Integration/AI/Platform skill with acceptance criteria and public seams defined.

Final merge still requires `team.reviewer.v1`.
