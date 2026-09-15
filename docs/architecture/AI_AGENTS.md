# AI Agent Architecture

## 1. Goal

Give Start agentic capabilities without turning an LLM into an unrestricted application runtime.

The platform has two agent contours:

1. **Interactive Employee Agent** — works on explicit human instruction.
2. **Routine Automation Agent** — works from configured workflow/event templates.

Both are read-first.

The model reasons over authorized evidence. Deterministic application services remain responsible for business state changes.

---

# 2. Shared agent runtime

Both contours use the same platform services:

~~~text
Agent Request / Trigger
        ↓
Agent Policy Resolver
        ↓
Authorization Scope
        ↓
Context Builder
        ↓
Read Capability Gateway
        ↓
Knowledge + Business Data
        ↓
LLM Reasoning
        ↓
Structured Result
        ↓
Draft / Action Proposal
        ↓
Deterministic Application / Workflow
~~~

Shared components:

- AgentDefinition;
- AgentRun;
- AgentPolicy;
- ToolPolicy;
- RetrievalPolicy;
- Prompt/TemplateVersion;
- StructuredOutputSchema;
- ActionProposal;
- ActionGateway;
- HumanReview/Approval;
- telemetry/audit.

---

# 3. Interactive Employee Agent

## Trigger

Explicit authenticated user instruction.

Examples:

- "Что происходило по дому за неделю?"
- "Найди все документы по этой аварии."
- "Собери историю обращения."
- "Подготовь ответ жителю."
- "Какие задачи у меня просрочены?"
- "Сравни этих двух подрядчиков."
- "Найди похожие юридические обращения."
- "Составь проект ответа на письмо прокуратуры."

## Scope

The agent inherits:

- user identity;
- selected organization/group context;
- effective permissions;
- object/business-unit restrictions;
- document/legal/financial restrictions.

The model cannot ask for broader access.

## Default capabilities

The agent should not receive one tool per table/entity.

Prefer a small stable surface.

### business.search

Search authorized structured entities.

Can cover:

- Cases;
- Incidents;
- WorkOrders;
- Tasks;
- Objects;
- Assets;
- Persons;
- Counterparties;
- Documents;
- Legal Cases;
- Financial projections;
- other registered entity types.

The application layer resolves the entity-specific query.

### business.get

Read one authorized entity/projected view by opaque reference.

### knowledge.search

Hybrid lexical/vector retrieval over authorized indexed evidence.

### timeline.read

Read event/history timeline for authorized entity/process.

### metrics.read

Read authorized metrics/aggregates.

### draft.create

Create a non-authoritative draft artifact, e.g.:

- reply;
- announcement;
- legal response draft;
- task description;
- summary.

Draft is not sent/published/executed automatically unless policy explicitly allows a later deterministic step.

### action.propose

Submit a typed proposal to Action Gateway.

It is not a raw generic write tool.

Examples:

- propose Case reassignment;
- propose deadline change;
- propose Task creation;
- propose status transition;
- propose sending a prepared notification.

The gateway decides whether the proposal is allowed, requires confirmation/approval, or must be rejected.

---

# 4. Routine Automation Agent

## Trigger

A deterministic workflow/event invokes an AgentDefinition.

Examples:

~~~text
communication.received
→ classify_intake agent

document.received
→ classify_legal_document agent

case.created
→ duplicate_candidate agent

incident.changed
→ draft_resident_update agent

month.closed
→ management_narrative agent
~~~

## Bounded task envelope

Every run receives a bounded envelope:

- organization_id;
- service identity;
- trigger event/entity;
- allowed entity/source classes;
- explicit input references;
- retrieval scope;
- agent definition/version;
- expected structured output;
- confidence policy;
- maximum tool calls;
- maximum runtime;
- token/cost budget;
- fallback/review policy.

It does not start with generic access to the entire tenant.

## Output

The routine agent returns structured output.

Example:

~~~json
{
  "classification": "water_leak",
  "priority": "urgent",
  "building_ref": "...",
  "duplicate_incident_candidate": "...",
  "confidence": 0.94,
  "evidence_refs": ["..."]
}
~~~

Workflow/application code then validates and applies allowed state changes.

## Typical jobs

- extraction;
- classification;
- matching;
- summarization;
- duplicate detection;
- prioritization suggestion;
- routing recommendation;
- drafting;
- anomaly explanation.

Routine agent should not become a replacement for deterministic SLA timers, permission checks, calculations or workflow transitions.

---

# 5. Action Gateway

## Purpose

One controlled path for all agent-initiated mutations.

~~~text
ActionProposal
    ↓
schema validation
    ↓
actor/service scope
    ↓
permission/policy
    ↓
business invariant
    ↓
idempotency
    ↓
confirmation/approval if required
    ↓
application service / workflow
    ↓
audit + result
~~~

## Action classes

Action classes are registered and versioned.

Examples:

- task.create;
- case.assign;
- case.transition;
- deadline.change;
- draft.publish;
- notification.send.

Do not expose arbitrary CRUD.

## Risk levels

Action policies can classify operations:

- read;
- draft;
- low-risk reversible write;
- controlled write;
- high-impact forbidden-to-agent.

High-impact default examples:

- bank payment execution;
- legal signature;
- membership/permission administration;
- secret rotation;
- destructive bulk deletion;
- tenant security configuration.

These are not ordinary agent capabilities.

---

# 6. Agent definitions are configuration

An AgentDefinition is versioned data.

Possible fields:

- contour: interactive | routine;
- name;
- purpose;
- prompt/template version;
- allowed read capabilities;
- allowed entity/source types;
- retrieval policy;
- allowed action proposals;
- output schema;
- confidence thresholds;
- model/provider policy;
- fallback model policy;
- max tool calls;
- max runtime;
- token/cost budget;
- human-review policy;
- enabled organizations/business units;
- status/version.

No business prompt/model/tool allowlist should require a code deploy for routine tuning.

System safety rules remain code/policy controlled and cannot be weakened by tenant prompts.

---

# 7. Read-first principle

Most agent value is achieved through:

- finding;
- joining context;
- summarizing;
- comparing;
- explaining;
- drafting;
- recommending.

Therefore default capability = read.

Write access is exceptional and always goes through Action Gateway.

Benefits:

- smaller attack surface;
- easier authorization;
- simpler testing;
- fewer accidental duplicate side effects;
- clearer audit;
- easier prompt-injection containment;
- better compatibility with multi-tenant RLS.

---

# 8. Retrieval strategy

Agents can combine:

## Structured retrieval

For exact business facts:

- status;
- deadline;
- amount;
- assigned person;
- SLA;
- metrics;
- identifiers.

## Knowledge retrieval

For unstructured evidence:

- contracts;
- letters;
- legal documents;
- manuals;
- communications;
- notes;
- reports.

The agent should prefer structured facts when the answer is a structured field.

Vector search is evidence discovery, not a replacement for relational queries.

---

# 9. Human confirmation

Interactive actions can follow configurable confirmation policies.

Examples:

### No confirmation

- read;
- search;
- summarize;
- create private draft.

### Explicit confirmation

- send resident notification;
- create/assign task;
- change deadline;
- move Case to a material state.

### Additional approval / step-up

- sensitive legal action;
- high-value approval;
- privileged configuration.

Routine automation uses its own pre-approved workflow policy instead of pretending a human confirmed each event.

---

# 10. Memory

## Interactive session memory

May retain short-term context inside one authorized conversation/session.

## Durable business memory

Must be stored as:

- domain entity;
- note/document;
- configuration;
- KnowledgeSource;
- other explicit persisted business record.

The model's hidden conversation memory is not a business database.

## Cross-tenant rule

No hidden agent memory can bridge companies without explicit group-authorized retrieval.

---

# 11. Observability

AgentRun records:

- run_id;
- contour;
- AgentDefinition/version;
- user/service identity;
- organization/group;
- trigger/instruction;
- model/provider;
- retrieval policy;
- tool calls;
- evidence refs;
- latency;
- tokens/cost;
- structured output;
- validation status;
- confidence;
- action proposals;
- confirmation/approval;
- final application result;
- fallback/retry;
- error class.

Sensitive content uses redaction/retention policy.

---

# 12. Testing strategy

## Shared runtime

Unit:
- policy resolution;
- tool allowlist;
- action risk classification;
- output schema validation.

Integration:
- authorization scope;
- RLS;
- Knowledge retrieval;
- Action Gateway;
- audit persistence.

Security:
- prompt injection;
- malicious retrieved document;
- cross-tenant entity reference;
- unauthorized tool request;
- scope widening attempt.

## Interactive Agent E2E

Happy path:

~~~text
employee logs in
→ asks about authorized Case
→ agent reads Case + timeline + documents
→ returns evidence-backed answer
~~~

Write proposal:

~~~text
employee asks "перенеси срок на завтра"
→ agent proposes deadline.change
→ Action Gateway checks permission
→ confirmation
→ workflow/application changes deadline
→ audit recorded
~~~

Permission failure:

~~~text
employee asks about another tenant
→ no unauthorized evidence retrieved
→ agent returns access-safe result
~~~

## Routine Agent E2E

Happy path:

~~~text
Communication received
→ configured agent run
→ read/context tools
→ typed classification
→ workflow validates
→ Case is classified/routed
~~~

Uncertainty path:

~~~text
agent confidence below policy
→ no automatic mutation
→ Human Review item created
~~~

Failure path:

~~~text
AI provider unavailable
→ bounded retries/fallback
→ deterministic/manual review state
→ no lost event
~~~

## Smoke

Use deterministic fake model/embedding provider so smoke does not depend on external AI availability.

Production provider checks are separate integration health tests.

---

# 13. Relationship to Owner AI

Owner AI uses **Interactive Employee Agent runtime** with group-authorized context.

It does not get a special hidden root toolset.

Differences are policy/scope/UI:

- group-level permissions;
- cross-company metrics;
- group-authorized Knowledge retrieval;
- management-oriented prompts/views;
- stronger authentication for sensitive actions.

---

# 14. Relationship to Property Management automation

Property Management features should reuse the routine contour for:

- inbound classification;
- entity extraction;
- Incident candidate matching;
- legal document classification;
- announcement drafting;
- monthly narrative drafting.

Deterministic components remain responsible for:

- Case numbering;
- SLA timers;
- state transitions;
- assignment rules once selected;
- authorization;
- notification delivery;
- financial calculations.

---

# 15. Design rule

When adding an AI feature, first ask:

> Can this be implemented with an existing read capability + structured result + deterministic workflow action?

If yes, do not add a new model tool.

A new tool/capability requires an architecture/security review when it materially increases write authority or data reach.
