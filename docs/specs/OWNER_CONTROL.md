# Owner Control Specification

## 1. Purpose

Owner Control is a separate management experience for people who own or oversee several businesses.

It must not be a renamed employee CRM dashboard.

The default question is:

> What in my authorized businesses requires my attention or decision?

## 2. Access model

A user authenticates globally.

Access comes from explicit GroupMembership and/or OrganizationMembership.

Example:

```text
User
├── Group A: group.analytics.read
├── Organization 1: finance.read
├── Organization 2: operations.drilldown
└── Organization 3: documents.read
```

An owner can log in from any supported device/location subject to security policy.

Tenant-branded entrypoints may redirect an authorized group-level user to Owner Control or allow a safe context switch.

## 3. Default landing page

Suggested sections:

### Group health

- organizations and health state;
- critical alerts;
- warnings;
- data freshness indicators.

### Money

Where integrations permit:

- balances;
- receivables/payables;
- cash-flow events;
- plan/fact;
- unusual spend;
- upcoming obligations.

### Risk / deviations

- project delays;
- SLA deterioration;
- incident spikes;
- cost anomalies;
- contractor underperformance;
- integration/data freshness failures.

### Decisions required

A short queue of high-level decisions requiring this user's permission/attention.

## 4. Progressive drill-down

```text
Group
→ Organization
→ Business Unit
→ Object/Project
→ Process/Case/Asset
→ Evidence/Timeline
```

Owner Control should preserve high-level context while allowing evidence inspection.

## 5. Company card

A normalized card despite different industries.

Potential common fields:

- health score/state;
- data freshness;
- revenue/cost summary where available;
- active critical risks;
- major projects;
- operational quality;
- staffing/capacity summary;
- key assets;
- contractor/supplier issues.

Vertical packs may add domain-specific sections.

## 6. Health scores

Scores are not universal magic numbers.

Each score has:

- definition;
- inputs;
- weights/rules;
- version;
- time window;
- confidence/data completeness.

Users can inspect “why this score”.

## 7. Owner AI

### Supported question classes

Examples:

- What needs my attention today?
- Why did costs rise this month?
- Which contractors are underperforming?
- Which objects generate repeat failures?
- Which assets are expensive to maintain?
- Where are we missing SLA?
- How much did we spend with counterparty X across the group?
- Which companies buy the same category independently?
- What changed since last week?

### Evidence requirement

Answers should cite/internal-link the underlying platform records/metrics where possible.

The system distinguishes:

- observed fact;
- calculated metric;
- configured threshold;
- model inference/recommendation.

### Authorization

AI retrieval is filtered before model context construction.

The model never receives unauthorized tenant data.

## 8. Cross-company counterparty intelligence

Resolve legal counterparties across organizations.

Show:

- organizations using the counterparty;
- total spend/receipts where authorized;
- contracts;
- performance;
- disputes/issues if stored;
- price differences for comparable items where data quality permits.

Entity matching must be evidence-based (e.g. legal identifier), not name similarity alone.

## 9. Cross-company procurement opportunities

Potential detection:

- same item/category bought independently;
- materially different price;
- duplicated vendors;
- frequent small purchases;
- avoidable emergency purchase patterns.

The platform suggests opportunities; it does not fabricate savings.

## 10. Asset intelligence

Across authorized organizations:

- high downtime;
- high repair cost;
- repeated failure;
- underutilization;
- maintenance due.

## 11. Attention hierarchy

Events should be reduced as they travel upward.

```text
raw events
→ operational exceptions
→ manager deviations
→ director risks
→ owner decisions
```

Do not notify an owner merely because an employee task is overdue unless policy/risk escalation warrants it.

## 12. Notification policy

Owner notifications are configurable by:

- severity;
- organization;
- metric;
- threshold;
- time window;
- channel;
- quiet hours;
- digest vs immediate.

## 13. Sensitive actions

Owner Control may eventually initiate:

- approval;
- delegation;
- budget decision;
- contract decision;
- payment request approval.

High-impact actions require:

- explicit permission;
- deterministic validation;
- complete audit;
- step-up authentication where policy requires;
- clear distinction between preparation and actual execution.

## 14. Data freshness

Every external-data panel displays freshness.

Example states:

- live/recent;
- delayed;
- stale;
- unavailable.

AI must account for stale data and disclose material freshness issues.

## 15. Mobile-first management

Owner Control should work effectively on desktop and mobile/PWA.

Mobile prioritizes:

- attention queue;
- company health;
- money/risk summary;
- AI question;
- approve/delegate;
- drill-down.

## 16. MVP

Owner Control Lite after the first tenant pilot:

- global identity;
- group/org switcher;
- organization cards;
- critical alerts;
- operational KPIs;
- cross-company structure even if only one tenant has rich data;
- AI summary over authorized normalized metrics.

Advanced finance/counterparty intelligence follows after integrations.
