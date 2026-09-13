# Gambit MCP implementation plan

Status: accepted for staged implementation; no stage grants production approval.

## Governing baselines

- Production template: `6526db4`, including the MCP Server Engineering Standard.
- Gambit review baseline: `9c550bdae592e975f12046ebbb8d690889fd9206`.
- MCP target: `2026-07-28`; Python SDK `2.2.0`; legacy-era compatibility is
  tested but may be removed by an approved compatibility ADR.

## Invariants

- Read-only research until a later plan explicitly approves a mutation.
- No live trading, broker connectivity, investment advice, arbitrary code,
  notebooks, callbacks, dynamic imports, caller paths, or arbitrary URLs.
- Protocol metadata and tool annotations are never security identities.
- Remote HTTP is not production-enabled until resource-server authorization,
  header/body parity, limits, isolation, and negative tests pass.
- Gambit capabilities retain their upstream supported/experimental labels.
- Failed or cancelled work cannot publish a successful partial result.

## Delivery gates

| Stage | Scope | Blocking exit evidence |
|---|---|---|
| M0 | Decisions and contracts | **Complete for local/no-data M1 boundary**; see `M0_SIGNOFF.md` |
| M1 | Walking skeleton | **Complete for local/no-data scope**; see `M1_SIGNOFF.md` |
| M2 | Market-data validation | Admitted format and semantic-profile contracts; Gambit adapter and independent golden cases; bounded hostile-input tests |
| M3 | Protected remote HTTP | OAuth resource-server metadata and challenges; token and object authorization; tenant isolation; header/body parity; distributed limits |
| M4 | Datasets, jobs, results | Trusted entitlement source; handle lifecycle; encryption; audit durability; idempotent jobs; atomic artifacts; restore/deletion tests |
| M5 | Declarative backtesting | Versioned allowlist and cost estimator; isolated workers; independent financial reconciliation; deterministic replay envelope |
| M6 | Production promotion | Client/host evals; load/soak; SBOM/provenance; canary/rollback; incident, correction, restore and key-rotation exercises |

## Accepted backlog from plan review

These are gates, not optional review notes. “P0” blocks only the named capability.

| ID | Blocks | Required decision/evidence |
|---|---|---|
| GAP-01 | Dataset admission | Per-ingestion-mode media/parser boundary, immutable object version, quarantine when uploading, hostile corpus |
| GAP-02 | Claimed-capability backtests | Versioned market-data semantic profile and quant/data-owner golden cases |
| GAP-03 | Dataset admission and result export | Trusted administrative entitlement authority and policy-enforcement matrix |
| GAP-04 | Deterministic-replay claims | Canonical serialization/environment envelope; byte identity versus financial tolerances; retained bytes or verified immutable external reference |
| GAP-05 | Durable jobs | Authorization checks at submit, dequeue, publish, read, export and cancel; revocation races |
| GAP-06 | Durable jobs and remote production | Separate tamper-resistant audit contract; operation-specific fail behavior and bounded spool |
| GAP-07 | Durable data | Key ownership, encryption and rotation; precise primary deletion, key destruction, backup expiry and legal-hold claims |
| GAP-08 | Result publication | Lineage and explicit under-review/invalidated/superseded access policy; correction drill |
| GAP-09 | Backtesting | Component registry, semantic validator and conservative cost estimator with adversarial cases |
| GAP-10 | Paginated results | Snapshot-bound cursor and concurrent disposition/deletion tests |
| GAP-11 | Durable jobs | Distinct transport-disconnect, MCP cancellation and job-cancellation semantics |
| GAP-12 | Multi-tenant scale | Fair scheduling, reservations/refunds and retry-storm evidence |
| GAP-13 | Rolling deployment | Contract digest, effective generation, N/N-1 discovery and job binding |
| GAP-14 | Data lifecycle | Copy inventory, deletion state machine and restore-tombstone drill |

## Current slice

M1 exposes only two static resources and `gambit_check_contract`. Its local
transport, execution-limit, interoperability, artifact and container gates pass
as recorded in `M1_SIGNOFF.md`. Remote production remains prohibited. Gambit is
intentionally not a runtime dependency until the M2 dependency/capability ADR is
approved.

## M0 progress

| Deliverable | Artifact | Status |
|---|---|---|
| Boundary and protocol | ADR-0001 | Accepted for M1 |
| Transport and compatibility | ADR-0002 | Accepted for SDK Client 2.2.0; other hosts gated |
| Authorization/principals | ADR-0003 | Local trust accepted; M3 expansion gated |
| Gambit dependency boundary | ADR-0004 | No-dependency M1 boundary accepted |
| Data admission/semantics | ADR-0005 | No-data M1 boundary accepted |
| Worker/state/isolation | ADR-0006 | Stateless/no-worker M1 boundary accepted |
| Project brief | `../PROJECT_BRIEF.md` | Approved for M0/M1 |
| Threat model | `../THREAT_MODEL.md` | Accepted for local/no-data M1 only |
| Latency/capacity budget | `LATENCY_BUDGET_M1.md` | M1 verification targets accepted |
| Requirement traceability | `REQUIREMENTS_TRACEABILITY.md` | Established |
| Accountable owner | `M0_SIGNOFF.md` | Repository owner for M0/M1 |

M0 is complete for the local, read-only, no-data M1 boundary. It does not approve
remote deployment or any Gambit/data/job capability. Those expansions retain the
specialist-owner and evidence gates recorded in their ADRs.

## Next changes

1. Define the M2 Polars/Arrow admission and market-data semantic profile.
2. Approve the Gambit adapter boundary and pin a published immutable artifact;
   never use a moving branch.
3. Add independent quant/data-owner golden cases and a bounded hostile-input
   corpus before exposing market-data validation.
