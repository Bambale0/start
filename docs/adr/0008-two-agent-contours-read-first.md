# ADR 0008 — Two AI Agent Contours with Read-First Tooling

**Status:** Accepted

## Context

Start needs AI that can help people work faster and also remove repetitive human relay work.

A single general-purpose agent with a large tool surface would create unnecessary security, predictability and audit risk, especially in a multi-company system containing legal, financial and personal data.

The platform already has deterministic workflow, authorization and knowledge/retrieval boundaries. Agent behavior should build on those boundaries rather than bypass them.

## Decision

Start uses two explicit AI agent contours.

### 1. Interactive Employee Agent

Human-in-the-loop agent invoked by an authenticated user.

It works on a user's explicit instruction, for example:

- find information;
- summarize a building/case/document;
- explain what happened;
- compare contractors;
- prepare a response;
- draft a document;
- suggest next actions;
- gather evidence for a legal/operational question.

The agent inherits the invoking user's effective tenant/group scope and permissions.

It is **read-first**.

Its default tool surface is intentionally small and capability-oriented rather than exposing dozens of entity-specific tools.

Representative capabilities:

- search/read authorized structured business data;
- search/read authorized knowledge/document evidence;
- read timelines/metrics;
- prepare a draft;
- propose a controlled business action.

Writes are not executed freely by the model.

A write goes through one controlled Action Gateway that:

1. validates permission;
2. validates tenant scope;
3. validates business rules;
4. shows/records the proposed action;
5. requires user confirmation when policy requires it;
6. invokes deterministic application/workflow services;
7. audits the result.

Owner AI is the same interactive-agent architecture with broader group-scoped permissions, not a separate privileged model.

### 2. Routine Automation Agent

Background agent invoked by a configured event/workflow template, not by open-ended human chat.

Examples:

- classify an incoming request;
- extract resident/address/problem;
- decide which configured routing rule candidate fits;
- detect a likely duplicate/Incident;
- summarize a document;
- draft a resident notification;
- classify incoming legal correspondence;
- assemble a monthly narrative from verified metrics.

It receives a **bounded task envelope**:

- tenant scope;
- triggering entity/event;
- allowed evidence sources;
- expected structured output schema;
- configured prompt/policy version;
- allowed action class;
- time/cost/tool budget.

It is also read-first.

The routine agent normally **returns a structured proposal/decision to Workflow Engine**. Deterministic workflow/application services perform mutations.

The routine agent should not directly own generic CRUD tools for business entities.

## Tool philosophy

Prefer a few stable capability tools over many narrow tools.

Conceptual read capabilities:

- `business.search`
- `business.get`
- `knowledge.search`
- `timeline.read`
- `metrics.read`

Conceptual controlled output/action capabilities:

- `draft.create`
- `action.propose`

These are architecture concepts, not fixed public API names.

Do not add a new model tool merely because a new entity type exists.

The application layer resolves entity-specific behavior behind stable capability contracts.

## Why read-first

Read-heavy agents are:

- easier to authorize;
- easier to audit;
- safer against prompt injection;
- easier to test;
- less likely to create duplicate or contradictory state;
- compatible with deterministic workflow execution.

Most useful employee requests are information synthesis, search, drafting and decision support.

Most routine automation can be expressed as structured decisions consumed by existing workflows.

## Action Gateway

All agent-initiated writes use a controlled gateway.

The gateway enforces:

- actor/service identity;
- organization/group scope;
- explicit action type;
- permission/policy;
- deterministic validation;
- idempotency key;
- optional confirmation/approval;
- workflow transition rules;
- audit;
- telemetry.

High-impact actions such as money movement, legal signature, membership changes or destructive actions are not available as ordinary agent tools.

## Memory

Agent memory is not a hidden cross-tenant store.

Long-lived knowledge belongs in authorized domain data / Knowledge Index.

Conversation/session state is scoped to:

- user/service identity;
- tenant/group;
- session/task;
- retention policy.

The model cannot create a new durable business fact merely by remembering it.

## Prompt and policy configuration

No hardcoded business prompts.

Agent definitions are versioned configuration containing:

- agent type;
- system policy/template;
- allowed capabilities;
- retrieval policy;
- structured output schema;
- confidence thresholds;
- tool/time/token/cost budget;
- human-confirmation policy;
- fallback behavior.

## Failure behavior

Interactive agent:

- disclose insufficient evidence;
- avoid fabricating records;
- propose clarification or safe next action;
- never silently widen scope.

Routine agent:

- return typed failure/uncertainty;
- retry only according to bounded policy;
- route to human review when confidence/policy requires it;
- never improvise unauthorized action.

## Observability

Every agent run records:

- run_id;
- agent definition/version;
- contour type;
- actor or service identity;
- organization/group scope;
- trigger/user instruction reference;
- retrieval/tool calls;
- model/provider;
- token/cost/latency;
- structured output validation;
- proposed action;
- confirmation/approval;
- final workflow/business result;
- errors/fallbacks.

Sensitive raw content follows retention/redaction policy.

## Testing

Both contours require:

- tenant/permission isolation;
- tool allowlist enforcement;
- prompt-injection fixtures;
- retrieval evidence tests;
- structured output validation;
- unavailable/timeout model behavior;
- deterministic fake-model adapter;
- action-gateway authorization;
- idempotent action execution;
- E2E authorized employee question;
- E2E unauthorized evidence absent;
- E2E routine event → proposal → workflow action;
- E2E low-confidence → human review;
- smoke with fake/deterministic AI provider.

## Consequences

The system gains agentic usefulness without turning the LLM into a privileged application runtime.

Adding a new business feature should usually add domain/application capability, not another direct LLM tool.
