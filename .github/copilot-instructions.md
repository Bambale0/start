# Repository Custom Instructions

Read AGENTS.md first.

Key rules:

- Treat Bambale0/skills as the primary engineering playbook.
- Read relevant docs and ADRs before editing.
- Keep the universal core industry-agnostic.
- Do not hardcode mutable business configuration.
- Enforce tenant scope server-side; never trust a browser-supplied organization ID alone.
- Owners are permission-scoped users, not hidden superusers.
- Keep provider payloads inside integration adapters.
- Add tests for behavior changes and regression fixes.
- Treat tenant-isolation failures as release blockers.
- Add logging/metrics/tracing for operationally important paths.
- Never commit secrets or real customer data.
- Do not claim tests/deployments you did not actually verify.
