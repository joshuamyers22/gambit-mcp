# ADR-0006: Worker, state, and isolation boundary

- Status: accepted as stateless/no-worker for M1; blocks durable jobs and backtests
- Date: 2026-09-13
- Owner: repository owner for M1; specialist owners required before M4/M5

## Context and options

Validation and backtests may invoke native parsers, consume substantial resources,
and outlive an HTTP request. They cannot safely execute in the MCP web process.

## Decision and consequences

- M1 has no application handles, queue, worker, artifact store, cross-call state,
  or expensive Gambit operation. The MCP process returns bounded static content.

- Keep synchronous admitted validation bounded; execute parsing/backtests in
  resource-restricted workers with no release/admin credentials and deny-default
  egress. Exact container/process platform remains open.
- Cross-call handles resolve through shared durable state reachable by every
  instance; do not use sticky sessions. Handles are high entropy, tenant/purpose-
  bound, expiring, revocable, quota-limited, and re-authorized on every use.
- Use `queued -> running -> succeeded | failed | cancelled | expired`; terminal
  states are immutable. Leases use fencing so a stale worker cannot publish.
- Stage artifacts under a unique generation and publish a verified manifest last.
- Separate MCP cancellation, transport disconnect, and durable job cancellation.
- Security audit is distinct from telemetry and has an approved bounded outage
  behavior. Encryption, retention, deletion, backup, restore and correction
  dispositions apply to every copy class.

## Verification and acceptance

M0 accepts the no-state/no-worker M1 boundary. M4/M5 acceptance requires the
selected queue/store/worker design, threat review,
duplicate/reorder/crash/cancel/publish races, resource-exhaustion tests, tenant
isolation, audit-sink failure, key rotation, deletion/restore, correction lineage,
RPO/RTO drills, and accountable owner approval.
