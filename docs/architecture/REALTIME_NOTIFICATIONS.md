# Realtime Communications and Priority Notifications

## 1. Goal

Start must not behave like a passive CRM that users have to refresh.

When something operationally important happens, the right person should see it immediately through the configured delivery surfaces.

This layer covers both:

1. **inbound near-real-time communications** — especially email and messengers;
2. **outbound priority notifications** — cases, urgent mail, incidents, SLA risk, approvals and other attention events.

"Immediate" means event-driven dispatch as soon as the platform observes the event. Exact delivery latency depends on the external provider/network and is measured rather than assumed.

---

# 2. Supported communication classes

Initial channels:

- in-app realtime;
- web/PWA push where available;
- email;
- MAX;
- Telegram;
- VK;
- SMS provider when configured;
- future mobile push;
- telephony-derived events.

Initial explicit email providers:

- Yandex Mail / Yandex 360 Mail;
- Mail.ru Mail;
- generic standards-compatible IMAP/SMTP mailbox.

Provider-specific connection details live in adapters/configuration and are verified against current provider documentation during implementation.

---

# 3. Email architecture

## EmailProvider port

Provider-independent capabilities:

- connect/test;
- list/watch mailbox;
- fetch message/thread;
- fetch attachments;
- mark processed where policy allows;
- send/reply;
- health/freshness;
- reconnect/resume cursor.

Adapters:

- YandexMailAdapter;
- MailRuAdapter;
- GenericImapSmtpAdapter.

## Authentication

Use the strongest provider-supported method.

Examples:

- OAuth/XOAUTH2 when available/configured;
- app-specific password where the provider/customer setup requires it.

Credentials are secret references and never stored/logged as normal configuration.

## Near-real-time ingestion

Preferred order:

1. provider webhook/push API, if officially available and appropriate;
2. IMAP IDLE/long-lived mailbox watch where supported;
3. adaptive short polling as fallback;
4. periodic reconciliation regardless of the primary mode.

The connection mode is adapter/configuration policy, not business logic.

### Why reconciliation still exists

Long-lived connections can disconnect and webhooks can be missed.

Therefore every mailbox tracks:

- provider message UID/ID;
- sync cursor;
- last observed timestamp;
- last successful watch event;
- last reconciliation;
- lag/backlog.

No email is considered safely ingested solely because a watch connection is alive.

---

# 4. Unified inbound pipeline

~~~text
Email / Messenger / Web / Phone event
            ↓
Communication
            ↓
priority pre-classification
            ↓
Routine Automation Agent / deterministic rules
            ↓
Case / Document / Task / LegalCase / Review
            ↓
Workflow
            ↓
Attention / Notification Engine
~~~

An inbound email is first persisted/normalized as Communication.

AI may classify and extract, but raw provider state, deduplication and workflow transitions remain deterministic.

---

# 5. Priority and attention model

Notifications are not a boolean "send or don't send".

Each business event can produce an **AttentionEvent** with configurable severity.

Conceptual levels:

- informational;
- normal;
- important;
- urgent;
- critical.

Labels and thresholds are tenant-configurable.

Examples:

### Normal

- new non-urgent Case assigned;
- ordinary task update.

### Important

- new official email requiring response;
- document waiting for approval;
- Case remains unaccepted longer than configured target.

### Urgent

- emergency Case;
- high-priority incoming email/document;
- SLA close to breach;
- failed critical integration;
- resident mass Incident.

### Critical

- active emergency requiring immediate escalation;
- critical process failed without an owner;
- configured severe safety/business event.

The application uses typed severity/risk, not keyword-only hardcode.

---

# 6. Notification policy

NotificationPolicy is versioned tenant configuration.

It may define:

- triggering event/type;
- severity;
- recipient role/user/team;
- organization/business-unit/object scope;
- preferred channels;
- fallback channels;
- quiet-hours behavior;
- urgent override;
- acknowledgement required;
- acknowledgement deadline;
- retry/backoff;
- escalation chain;
- digest vs immediate;
- deduplication window;
- rate limiting;
- message template;
- grouping policy.

Example:

~~~text
IF
  event = case.created
  AND severity >= urgent
THEN
  send in-app immediately
  + push
  + messenger to on-duty dispatcher
  require acknowledgement
  if no ACK within configured window
      escalate to area manager
~~~

No threshold/minutes/recipients are source-code constants.

---

# 7. In-app realtime

For authenticated office users, critical operational updates should appear without manual page refresh.

Target architecture:

~~~text
Domain Event
→ Notification/Attention worker
→ authorized recipient resolution
→ realtime transport
→ browser/PWA
→ update badge/toast/work queue
~~~

Transport may use WebSocket or SSE according to implementation ADR/performance needs.

The client remains a projection: backend state is authoritative.

Reconnect requires cursor/event recovery so a temporary browser disconnect does not lose notifications.

---

# 8. Acknowledgement and escalation

Urgent events may require explicit acknowledgement.

An acknowledgement records:

- AttentionEvent;
- recipient;
- time;
- channel/session;
- actor;
- optional comment/action.

If configured acknowledgement does not occur:

~~~text
notify
↓
wait durable timer
↓
no acknowledgement
↓
escalate
↓
notify next role/person/channel
~~~

Escalation is driven by Workflow/Timer infrastructure and survives restarts.

---

# 9. Urgent email

Not every new email should interrupt a user.

Inbound mail can be prioritized using:

- mailbox/address configuration;
- sender/counterparty;
- known official source;
- subject/body rules;
- linked object/case;
- document type;
- deadline extraction;
- Routine Automation Agent classification;
- configured VIP/authority categories.

High-confidence urgent classification can create an AttentionEvent automatically.

Low confidence routes to a review queue rather than fabricating urgency.

Examples:

- прокуратура/суд/официальное требование;
- аварийное уведомление;
- time-sensitive contractor issue;
- customer/resident escalation;
- integration/provider incident mail.

The exact categories are organization configuration.

---

# 10. Case notifications

At minimum support configurable attention on:

- new Case;
- emergency Case;
- Case not accepted;
- deadline assigned/changed;
- SLA warning;
- SLA breach;
- WorkOrder blocked;
- completed awaiting verification;
- reopened;
- Incident created/expanded.

Resident-facing notifications and employee attention events use the same domain events but different policies/recipients/templates.

---

# 11. Deduplication and anti-noise

Instant notification does not mean notification spam.

The engine must support:

- same-event idempotency;
- coalescing repeated updates;
- Incident-level grouping;
- cooldown/rate limiting;
- digest for low-priority events;
- urgent bypass according to policy;
- per-user unread/ack state.

Example:

100 resident Cases linked to one Incident should not produce 100 urgent messages to the same dispatcher unless explicitly configured.

---

# 12. Delivery states

Each delivery attempt tracks:

- queued;
- sent-to-provider;
- provider-accepted;
- delivered when provider exposes it;
- read/acknowledged when supported;
- retrying;
- failed;
- expired;
- superseded/grouped.

Do not claim "delivered" when the provider only accepted the request.

---

# 13. Observability

Track:

- inbound mailbox lag;
- watch connection state;
- reconnect count;
- reconciliation lag;
- message ingestion latency;
- dedup count;
- AttentionEvent creation latency;
- event → dispatch latency;
- provider send latency;
- delivery/failure;
- acknowledgement latency;
- escalation count;
- notification suppression/grouping;
- unread urgent count.

Potential SLOs are set after measuring production traffic, not invented in advance.

---

# 14. Security

- mailbox credentials are secret references;
- email tenant mapping is server-controlled;
- sender content is untrusted;
- attachments use document security pipeline;
- AI classification cannot widen recipient permissions;
- notifications contain only data the recipient may access;
- notification deep links re-authorize on open;
- revoked users stop receiving new notifications;
- delivery logs avoid leaking sensitive full content by default.

---

# 15. Testing

## Email adapters

Contract tests for Yandex, Mail.ru and generic IMAP/SMTP:

- authentication;
- connection loss/reconnect;
- fetch;
- attachment;
- duplicate UID/message;
- cursor resume;
- timeout;
- provider auth failure;
- outbound send/reply;
- rate/failure normalization.

Provider-specific live/sandbox checks are separate from deterministic CI.

## Near-real-time watch

- new message observed once;
- disconnect → reconnect;
- message received during disconnect recovered by reconciliation;
- duplicate watch + reconcile event remains one Communication;
- backlog metrics.

## Notification engine

Unit:
- policy matching;
- severity;
- recipient resolution;
- grouping;
- acknowledgement/escalation rules.

Integration:
- DomainEvent → AttentionEvent → Delivery;
- tenant/permission filters;
- durable timer;
- idempotency.

E2E:
1. new urgent Case → dispatcher receives in-app event without refresh;
2. urgent email → classified → responsible receives attention;
3. unacknowledged urgent event → escalation;
4. ordinary update → no urgent interruption;
5. mass Incident → grouped notification;
6. unauthorized user never receives event/content.

Smoke:
- clean stack;
- fake email provider emits message;
- platform ingests it;
- fake realtime subscriber receives expected alert;
- fake outbound provider records delivery;
- reconnect/reconciliation scenario.

---

# 16. Product rule

The goal is not "notify everywhere".

The goal is:

> important information reaches the right person immediately, routine information stays quiet, and nothing critical disappears because nobody refreshed a page.
