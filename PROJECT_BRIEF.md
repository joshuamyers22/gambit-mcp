# Project Brief

Status: approved by the repository owner for M0 and local M1 development on
2026-09-13. This is not remote-deployment or production approval.

- Problem and affected users: quantitative researchers need a bounded MCP surface
  for Gambit research workflows without arbitrary code, path, URL, or trading access.
- Measurable success criteria: the declared MCP client/protocol matrix passes;
  every exposed workflow has schemas, limits, authorization, audit, and independent
  domain evidence; clean builds and exact deployed artifacts are reproducible.
- Explicit non-goals: live trading, brokerage connectivity, investment advice,
  uploaded code/notebooks/callbacks, arbitrary filesystem or network access, and
  presenting experimental Gambit capabilities as production-ready.
- Runtime/deployment environment: Python 3.11+; trusted local stdio first;
  authenticated Streamable HTTP in a later approved milestone.
- Data classification and retention: assume market data, strategies, positions,
  and results are confidential. The walking skeleton accepts none of them.
- Availability and recovery objectives: no production SLO until remote deployment
  is approved. Configuration is reconstructed from version control and artifacts.
- Latency distribution, peak throughput, queue limits, and overload behavior:
  M1 defaults are 1 MiB requests, 64 KiB responses, eight concurrent calls, and
  30-second tool deadlines; production-like measurements remain required.
- Top failure or abuse scenarios: cross-tenant access, arbitrary code/path/URL
  access, prompt injection, resource exhaustion, token confusion, parser/native
  compromise, telemetry leakage, incorrect financial output, supply-chain attack.
- Authentication and authorization boundary: stdio inherits a documented trusted
  launcher boundary. Remote HTTP is disabled for production until resource-server
  metadata, token validation, per-operation authorization, and negative tests pass.
- Request/body/rate/concurrency limits: numeric defaults are configuration-validated;
  enforcement and distributed limiting block remote production.
- Dependency deadlines, retries, and idempotency: no upstream calls or writes in M1.
- SLI/SLO and alert ownership: repository owner during local M1 development;
  accountable operations/on-call ownership blocks remote production promotion.
- Replay or load-test evidence and performance-regression policy: contract tests
  cover both protocol eras; load/replay thresholds remain open.
- Deployment, migration, rollback, and recovery: immutable container workflow from
  the template; production deployment is not authorized by this brief.
- Owner: repository owner for M0/M1. Specialist approvals remain mandatory at
  the capability gates recorded in `docs/PROJECT_PLAN.md`.
