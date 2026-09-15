# Product and Automation KPIs

## Purpose

Start must prove operational value with measured outcomes rather than feature count.

## Core automation KPIs

### Human Intervention Rate

Percentage of eligible process instances that require a human touch.

```text
human-intervention processes / eligible processes
```

Track by:

- organization;
- process type;
- channel;
- automation rule;
- time period.

### Automation Rate

Percentage of eligible routine actions successfully completed without human execution.

### Human Touches per Case

Average number of manual actions required to reach completion.

A manual action should be defined consistently and instrumented, not inferred from clicks alone.

## Speed KPIs

- Intake Time: inbound event → structured Case;
- Routing Time: Case created → assignee determined;
- Acceptance Time: assignment → accepted;
- Resolution Time;
- Verification Time;
- End-to-End Cycle Time.

Use percentiles (p50/p90/p95), not only averages.

## Quality KPIs

- SLA compliance;
- reopen rate;
- repeat incident rate;
- duplicate-case rate;
- cancellation rate;
- failed automation rate;
- human correction rate after AI classification;
- customer feedback where available.

## Cost KPIs

- estimated cost per case/process;
- labor touches per unit;
- contractor cost;
- material cost;
- asset downtime cost;
- rework cost.

Do not present estimated savings as accounting facts. Label assumptions and calculation method.

## Management KPIs

### Management Attention Required

Number of events/decisions escalated to each management layer.

Goal: the higher the role, the fewer low-value events reach it.

Track separately for:

- manager;
- director;
- owner.

### Object Health Score

A configurable composite index from observable measures. Never hardcode one universal formula.

Potential inputs:

- incident rate;
- repeat failures;
- SLA;
- costs;
- complaints;
- asset state.

The configured formula, weights and version must be auditable.

### Contractor Score

Configurable metric composed from:

- cost;
- timeliness;
- SLA;
- rework;
- complaints;
- acceptance quality.

## Baseline requirement

Before automation rollout, capture a baseline for the same process.

At minimum:

- volume;
- manual touches;
- intake time;
- routing time;
- missed/duplicate requests;
- staffing;
- SLA.

## Experiment reporting

Every claimed improvement should state:

- measurement window;
- eligible sample;
- baseline;
- post-change result;
- exclusions;
- known confounders.

This prevents product demos from turning into ungrounded ROI claims.
