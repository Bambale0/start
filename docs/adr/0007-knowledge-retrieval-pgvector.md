# ADR 0007 — Derived Knowledge Index with pgvector First

**Status:** Accepted

## Context

Start will accumulate large volumes of unstructured and semi-structured information:

- resident and customer communications;
- building passports;
- contracts;
- EDO documents;
- legal correspondence;
- court/prosecutor-office materials;
- estimates;
- work reports;
- manuals/instructions;
- asset documents;
- policies/regulations;
- internal knowledge;
- future documents from other vertical packs.

Owner AI, employee search, legal search, duplicate detection and document assistance need semantic retrieval.

The vector/search layer must not become a second uncontrolled source of truth or a route around tenant permissions.

## Decision

Use a provider-agnostic Knowledge/Retrieval module.

Initial storage implementation: **PostgreSQL + pgvector**, combined with PostgreSQL full-text search for hybrid retrieval.

The vector index is **derived and rebuildable**.

Authoritative data remains:

- original binary → object storage / external source of record;
- document metadata and permissions → PostgreSQL domain records;
- legal original/signature state → EDO provider where applicable;
- knowledge chunks/embeddings → derived retrieval index.

A future dedicated vector engine such as Qdrant may be introduced behind the same retrieval port when measured scale, latency, memory, independent scaling or retrieval requirements justify it.

## Knowledge pipeline

```text
Source document / communication
        ↓
authorization + source metadata
        ↓
parse / normalize
        ↓
chunk
        ↓
embedding
        ↓
index
        ↓
hybrid retrieval
        ↓
rerank / evidence filter
        ↓
authorized result
        ↓
AI or user search
```

## Core retrieval records

### KnowledgeSource

Reference to the authoritative entity/document/communication.

### KnowledgeChunk

Derived text chunk with:

- organization_id;
- optional group_id;
- source type/id;
- source version/checksum;
- chunk ordinal;
- normalized text;
- metadata;
- permission scope;
- parser/chunker version;
- lifecycle state.

### EmbeddingRecord

Derived vector state with:

- chunk_id;
- embedding provider/model identifier;
- embedding dimension;
- embedding policy version;
- created_at;
- stale/rebuild state.

Embedding model names and dimensions are configuration, not hardcoded domain policy.

## Tenant and permission rule

Every tenant-bound chunk carries organization_id directly.

Retrieval applies authorization filters **before results enter AI context**.

Vector similarity never overrides:

- organization scope;
- group scope;
- object/document permissions;
- legal/sensitive-data permissions.

Database RLS and application authorization both apply where relevant.

## Hybrid retrieval

Default design supports both:

- lexical/full-text search;
- semantic/vector search.

The retrieval service may combine/rerank results.

The ranking method and weights are configuration/versioned policy when exposed to runtime tuning.

## Freshness and rebuild

Index state is tied to source checksum/version.

When a source changes:

1. previous derived chunks are marked stale;
2. new parse/chunk/embed job is queued;
3. new index version becomes active only after successful processing;
4. stale derived rows can be removed safely.

Deletion/access revocation propagates to retrieval immediately or fails closed.

## AI safety

External document text is untrusted content.

Retrieved chunks are evidence, not instructions.

Prompt/tool policy is never taken from retrieved document content.

## Observability

Track:

- ingestion jobs;
- parsing failures;
- chunk count;
- embedding latency/cost;
- index freshness;
- retrieval latency;
- candidate count;
- filtered result count;
- tenant/scope;
- retrieval policy/version;
- source references returned;
- reindex backlog.

Do not log full sensitive chunk text by default.

## Testing requirements

- tenant-isolation retrieval tests;
- permission filter tests;
- stale/rebuild tests;
- source deletion/revocation tests;
- hybrid lexical + vector behavior fixtures;
- deterministic test embedding adapter;
- idempotent re-index tests;
- malformed/unsupported document handling;
- prompt-injection content treated as data;
- E2E authorized search;
- E2E unauthorized cross-tenant query returns no evidence;
- smoke extension/index availability.

## Consequences

Positive:

- reuses existing PostgreSQL security/backup/operational model;
- avoids premature extra infrastructure;
- supports semantic and hybrid search;
- index can be rebuilt from authoritative sources.

Trade-offs:

- vector workload shares PostgreSQL resources;
- ANN index tuning requires monitoring;
- very large retrieval workloads may later need independent scaling.

Migration to a dedicated vector store must preserve the provider-agnostic retrieval contract and authorization semantics.
