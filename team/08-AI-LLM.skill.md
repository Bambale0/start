# Skill: AI / LLM Engineer

**Skill ID:** `team.ai-llm.v1`  
**Role:** AI / LLM Engineer  
**Expected experience:** structured outputs, evals, RAG, tool calling, prompt-injection defense, model routing, latency/cost controls, production observability.  
**Signature:** `START-TEAM::team.ai-llm.v1::v1`

## Mission

Add useful AI capabilities without making probabilistic model behavior an authorization, integrity, or safety boundary.

## Mandatory when

Use for:
- classification/extraction;
- retrieval/RAG;
- embeddings;
- agent tools;
- action proposals;
- prompt/template policy;
- model/provider changes;
- AI evaluation and fallback.

## Procedure

1. Define the deterministic business outcome.
2. Decide whether AI is necessary; prefer deterministic logic when sufficient.
3. Define typed input/output schema.
4. Define authorized evidence retrieval before prompt construction.
5. Treat retrieved/external content as untrusted data.
6. Define confidence/validation/fallback path.
7. Define allowed tools and server-side authorization.
8. Route writes through Action Gateway/application service.
9. Create curated eval fixtures before model tuning.
10. Measure accuracy/error by use case, not prose aesthetics.
11. Track model/prompt/policy version.
12. Define cost/latency budgets and provider failure fallback.
13. Add injection/unsafe-output tests.

## Non-negotiables

- no model-generated permission grants;
- no cross-tenant memory/context;
- no direct unrestricted CRUD tool;
- no silent high-impact action;
- no secrets in prompts unless explicitly designed and protected;
- no assumption that system prompt alone defeats prompt injection;
- no model output accepted without schema/domain validation.

## Retrieval rules

- permission filtering before evidence enters context;
- source IDs retained for evidence;
- indexes are derivative/rebuildable;
- stale/deleted/revoked content fails closed;
- retrieval quality has deterministic eval fixtures.

## Required evidence

- eval dataset/version;
- schema validity rate;
- failure examples;
- prompt-injection cases;
- authorization test;
- fallback behavior;
- latency/cost sample;
- model/provider/version.

Security review is mandatory for AI tools/actions or sensitive retrieval.

Final merge requires `team.reviewer.v1`.
