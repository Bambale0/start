# Integration Architecture

## 1. Principle

Start should feel like one business window without pretending to replace every specialized system.

The platform orchestrates systems of record through typed adapters.

## 2. Source-of-truth matrix

| Data class | Primary source of record | Start's role |
|---|---|---|
| Operational workflows/cases/tasks | Start | master |
| Workflow/business configuration | Start | master |
| Authorization/memberships | Start | master |
| Statutory accounting | 1C/accounting system | mirror + orchestrate |
| Legally significant EDO original | EDO provider | index + workflow |
| Bank balances/transactions | Bank | mirror + reconcile |
| Communication provider delivery facts | Provider | normalize + track |
| Management analytics | Start | derive/aggregate |

## 3. Integration port model

Provider-independent ports:

```text
AccountingProvider
EDOProvider
BankProvider
EmailProvider
TelephonyProvider
MessengerProvider
StorageProvider
IdentityProvider (optional federation)
```

Provider adapters implement those contracts.

Domain/application code depends on ports, not provider SDKs.

## 4. Connection model

Each tenant configures `IntegrationConnection`:

- organization;
- provider;
- capabilities;
- status;
- credential reference;
- non-secret config;
- mapping config;
- health;
- last successful sync.

No provider account is globally assumed.

## 5. Synchronization modes

### Pull

Scheduled/incremental fetch.

### Push

Start sends a requested mutation.

### Webhook

Provider emits an event.

### Reconciliation

Periodic comparison detects missed/drifted state.

Critical integrations should combine webhooks with reconciliation where feasible.

## 6. Idempotency

Every retriable mutating operation needs an idempotency strategy.

Use:

- Start operation ID;
- provider idempotency key where supported;
- external reference mapping;
- deduplication state.

Never “retry POST until it works” blindly.

## 7. Integration state

Expose explicit status:

```text
Connected
Degraded
AuthenticationRequired
RateLimited
Syncing
Failed
Disabled
```

Users should see stale data as stale.

Do not silently show an old bank/accounting value as current.

## 8. Accounting / 1C

### Initial phase: read-first

Import/mirror:

- counterparties;
- contracts;
- invoices/documents as appropriate;
- payments;
- receivables/payables;
- cost facts;
- relevant reference data.

### Later controlled writes

Possible:

- approved payment request;
- approved counterparty;
- operational document;
- order/request.

Writes require deterministic validation and reconciliation.

### Rule

Never write directly into an undocumented 1C database schema.

Use supported exchange/API mechanisms appropriate to the specific deployment and document each connector contract.

## 9. EDO

The EDO provider remains source of the legally significant original/signature status.

Start provides:

- unified inbox;
- metadata extraction;
- linked workflow;
- approval routing;
- signature-status visibility;
- links/references;
- mismatch/risk checks.

Potential providers are adapters, not core concepts.

## 10. Banks

### Phase 1

Read-only:

- accounts;
- balances;
- transactions;
- statements.

### Phase 2

Prepare/create payment instructions where provider/API allows.

### Phase 3

High-control approval/confirmation flows only after security maturity.

Start must clearly distinguish:

- observed completed payment;
- drafted payment;
- submitted payment;
- bank-accepted;
- bank-rejected.

## 11. Email

Email becomes a Communication source.

Pipeline:

```text
Email received
→ normalize
→ resolve tenant/mailbox
→ AI/deterministic extraction
→ entity resolution
→ Case/Document/Task
→ workflow
```

Raw mail remains retrievable according to provider/storage policy.

## 12. Telephony

Pipeline:

```text
Call
→ provider event
→ recording/transcript where lawful/configured
→ person/object resolution
→ Case/Incident
→ workflow
```

Call recording/retention is tenant-policy and jurisdiction dependent.

## 13. Messengers

MAX/Telegram/VK and future channels are adapters.

They should not own:

- CRM state;
- permissions;
- business categories;
- workflow definitions;
- AI prompts;
- SLA rules.

## 14. Integration observability

For each call/sync record:

- provider;
- connection;
- organization;
- operation type;
- correlation ID;
- start/end;
- latency;
- result class;
- provider status/error code;
- retry count;
- rate-limit data where safe;
- external object/event ID.

Do not log secrets or full sensitive payloads by default.

## 15. Failure semantics

Every integration contract defines:

- retryable failure;
- permanent failure;
- auth failure;
- rate limit;
- conflict;
- duplicate;
- unknown result.

Unknown-result mutations trigger reconciliation, not blind re-execution.

## 16. Adapter testing

Each provider requires:

- unit tests for mapping;
- contract fixtures;
- signature/webhook tests;
- idempotency tests;
- timeout/retry tests;
- sandbox integration tests where available.
