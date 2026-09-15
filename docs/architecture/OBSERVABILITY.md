# Observability and Operational Telemetry

## 1. Principle

If production behavior cannot be reconstructed from telemetry, the feature is incomplete.

Observability covers both technical health and business-process health.

## 2. Correlation fields

Propagate wherever relevant:

- request_id;
- trace_id;
- span_id;
- user_id;
- organization_id;
- group_id;
- case_id;
- incident_id;
- work_order_id;
- workflow_instance_id;
- integration_connection_id;
- provider correlation/event ID.

Personal/sensitive fields are not correlation substitutes.

## 3. Structured logging

Use structured logs.

Recommended common fields:

```text
timestamp
level
service
environment
event
request_id
trace_id
organization_id
actor_id
entity_type
entity_id
duration_ms
result
error_class
```

Do not log:

- access tokens;
- passwords;
- private keys;
- full bank credentials;
- complete sensitive documents;
- unnecessary raw personal communications.

## 4. Tracing

Instrument:

- HTTP request lifecycle;
- DB queries/transactions at safe granularity;
- queue publish/consume;
- workflow actions;
- AI calls;
- external providers;
- notification delivery.

Use OpenTelemetry-compatible APIs/exporters to avoid vendor lock-in.

## 5. Technical metrics

Examples:

- request rate/error/latency;
- DB pool saturation;
- query latency;
- queue depth/age;
- worker throughput;
- retry rate;
- integration error rate;
- webhook lag;
- AI provider latency/error/token usage;
- cache hit/miss where relevant.

## 6. Business-process metrics

Examples:

- inbound volume;
- automation rate;
- human intervention;
- intake latency;
- assignment latency;
- SLA breach;
- case backlog;
- incident volume;
- work-order completion;
- reopen/rework;
- notification delivery;
- document approval latency;
- integration reconciliation drift.

## 7. Audit vs logs

Audit and logs are not the same.

Logs answer operational diagnosis.

Audit answers who changed/did what and must have stronger retention/integrity guarantees.

## 8. Integration health dashboard

Each connection exposes:

- last successful request;
- last successful sync;
- current auth state;
- failure streak;
- rate-limit state;
- backlog;
- reconciliation drift;
- data freshness.

## 9. Workflow observability

Every workflow instance exposes a timeline:

```text
triggered
classified
assigned
timer scheduled
reminder sent
escalated
completed
verified
```

Each step includes reason/actor/system component.

## 10. AI observability

Track safely:

- model/provider;
- use-case;
- prompt/template version;
- latency;
- token/cost data;
- parsed output success;
- confidence where meaningful;
- human correction;
- fallback/escalation;
- policy decision.

Avoid storing raw sensitive prompts indefinitely by default.

## 10A. Knowledge/retrieval observability

Track:

- ingestion jobs and backlog;
- parser/chunker version;
- parse failures;
- source-to-chunk count;
- embedding profile/model;
- embedding latency/cost/failures;
- stale chunks;
- reindex queue age;
- retrieval latency;
- lexical/vector candidate counts;
- post-permission filtered counts;
- rerank latency;
- returned evidence source IDs;
- retrieval policy/version;
- recall/quality evaluation on curated fixtures.

Do not log full sensitive chunk text by default.

Monitor approximate-search quality against deterministic evaluation fixtures before changing vector index parameters.

## 11. Alerts

Alerts should be actionable.

Technical examples:

- sustained 5xx;
- queue age threshold;
- webhook failures;
- DB saturation;
- provider auth broken.

Business examples:

- SLA breach spike;
- missed inbound ingestion;
- abnormal automation failure;
- reconciliation drift;
- management anomaly.

Thresholds are configurable.

## 12. SLO direction

Define SLOs once baseline traffic exists.

Candidate SLI classes:

- API availability;
- inbound ingestion success;
- workflow execution latency;
- notification delivery;
- integration freshness;
- owner dashboard freshness.

Do not invent percentage targets before operational evidence and business criticality are understood.

## 13. Incident workflow

Production incidents should capture:

- start/end;
- affected organizations;
- affected capabilities;
- customer impact;
- detection source;
- root cause;
- mitigation;
- permanent fix;
- regression test;
- telemetry improvement.

Every serious incident should leave the system easier to diagnose next time.
