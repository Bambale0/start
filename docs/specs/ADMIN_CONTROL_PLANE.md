# Admin / Control Plane Specification

## 1. Goal

Routine business configuration must be changeable without editing code, SQL or deployment files.

The control plane is the management surface for platform/tenant configuration.

## 2. Scope separation

### Platform admin

Manages platform-wide technical capabilities where authorized.

### Group admin

Manages group-level memberships/policies.

### Organization admin

Manages tenant-specific users, configuration, vertical pack settings and integrations.

Never imply that every local admin can modify global platform state.

## 3. Required configurable areas

### Organization

- name/branding;
- locale/timezone;
- enabled vertical packs;
- feature/capability flags;
- business units.

### Users/access

- memberships;
- roles;
- permissions;
- status;
- validity windows;
- business-unit/object scope.

### Taxonomies

- case types;
- categories;
- statuses;
- priorities;
- reason codes;
- tags.

### Workflows

- definitions;
- versions;
- trigger;
- conditions;
- actions;
- assignments;
- timers;
- approvals;
- escalations.

### SLA

- profiles;
- applicability rules;
- timers;
- escalation policies.

### Communications

- channels;
- mailboxes/numbers/accounts;
- templates;
- routing;
- notification policies.

### AI

- provider/model policies;
- use-case configuration;
- prompt/template versions;
- confidence policy;
- human-review policy;
- allowed tools/actions.

Secrets are referenced, not exposed.

### Integrations

- connections;
- capabilities;
- credentials replace/rotate;
- mappings;
- enable/disable;
- sync schedule;
- health/test;
- reconciliation.

### Scoring/analytics

- metric definitions;
- score definitions;
- alert thresholds;
- dashboard presets.

## 4. Configuration publication

High-impact configuration should support draft/publish/version semantics.

Examples:

- workflow definitions;
- score definitions;
- routing rules;
- AI policy.

A published version is immutable for historical reproducibility.

## 5. Validation

The admin must prevent invalid publication.

Examples:

- workflow contains unreachable/invalid step;
- role references removed permission;
- SLA escalation has no valid target;
- integration mapping references nonexistent object type;
- owner score uses unavailable metric.

## 6. Preview/testing

Where practical:

- workflow dry run;
- routing simulation;
- notification preview;
- integration connection test;
- AI extraction/classification test on safe sample;
- score preview.

## 7. Audit

Every material configuration mutation records:

- actor;
- timestamp;
- scope;
- object;
- before/after or version;
- publish result.

## 8. Secret UX

Allowed actions:

- add;
- replace;
- rotate;
- test;
- revoke.

Never display the stored plaintext secret after save.

## 9. Import/export

Longer-term:

- export configuration pack;
- import into another organization;
- validate differences;
- environment promotion.

Secrets are excluded.

## 10. Safety

Dangerous changes can require:

- confirmation;
- second approval;
- step-up auth;
- scheduled effective time.

The policy is configurable according to risk.
