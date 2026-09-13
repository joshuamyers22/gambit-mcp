# Gambit MCP engineering standard

This is the project-tailored gate derived from
`production-project-template/templates/MCP_SERVER_ENGINEERING_STANDARD.md` at
`6526db4`. It accepts that template's Section 17 corrections: resource-server
OAuth duties are separated from client duties, authentication is transport-
specific, application handles may require shared state, modern metadata rules
match the final revision, and HTTP routing headers must match the body.

Requirement labels are `SPEC`, `SECURITY`, or `PROJECT`. MUST items block the
affected production capability. SHOULD items require a recorded deviation with
owner, approver, compensating control, residual risk, and expiry.

## Server profile

| Field | Value |
|---|---|
| Server | `gambit-mcp` 0.1.0 |
| Purpose | Bounded read-only Gambit research workflows for MCP agents |
| Upstream | None in M1; approved `gambit-markets` public API beginning in M2 |
| Target revision | `2026-07-28` |
| SDK | Python MCP SDK `2.2.0` |
| Compatibility | MCP Python SDK Client 2.2.0: modern target plus tested `2025-11-25` compatibility path; other hosts unsupported |
| Transport | Trusted local stdio; localhost Streamable HTTP for development/conformance only |
| Authorization | Stdio launcher trust in M1; remote OAuth resource server not implemented |
| Data | No user/market data admitted in M1; future data presumed confidential |
| Writes | None |
| Owner | Repository owner for M0/M1; specialist ownership required by later gates |
| Last reviewed | 2026-09-13 |

## Blocking requirements

- [x] **SPEC** Target revision and exact SDK are declared and locked.
- [x] **SPEC** New code does not use Roots, Sampling, protocol Logging, DCR, or
  legacy HTTP+SSE.
- [x] **PROJECT** Tools use the `gambit_` namespace and describe when not to use them.
- [x] **SECURITY** M1 has no implicit cross-call state, upstream token forwarding,
  arbitrary paths/URLs, or code execution.
- [x] **PROJECT** Tool results are typed and bounded; resources are deterministic.
- [x] **SECURITY** Local HTTP binds to `127.0.0.1` by default.
- [x] **PROJECT** Explicit request, response, concurrency and timeout values exist.
- [x] **SPEC** Modern and legacy-era in-process client contracts are tested.
- [x] **SPEC** Real-process tests verify modern request metadata and negotiated
  response `serverInfo`. Streamable HTTP `Mcp-*` parity remains an M3 gate.
- [x] **SECURITY** Enforce request/argument/response/time/concurrency limits at
  every active transport boundary; configuration alone is not evidence.
- [x] **SECURITY** Capture stdio and prove stray application output cannot corrupt
  stdout; diagnostics and telemetry must use stderr.
- [x] **PROJECT** Run MCP Inspector and retain the commands/result in
  `M1_SIGNOFF.md`.
- [ ] **PROJECT** Maintain realistic model evals with held-out tasks, repeated
  trials, trajectory grading, task success and token-cost thresholds (M6 before
  production promotion; M1 has no real research workflow to evaluate).
- [x] **PROJECT** Define the initial supported client/host matrix and compatibility
  policy. Adding any host requires its own contract evidence.

## Gates before protected remote HTTP

- [ ] **SPEC** Publish RFC 9728 Protected Resource Metadata and correct
  `WWW-Authenticate` challenges.
- [ ] **SECURITY** Validate token signature, issuer, audience/resource, expiry,
  not-before, algorithm and scopes on every protected request.
- [ ] **SECURITY** Define user, tenant, client application, workload/agent and
  service identities; never use self-reported `clientInfo` for authorization.
- [ ] **SECURITY** Enforce object-level authorization and negative cross-tenant tests.
- [ ] **SPEC** Validate `Mcp-Method`, `Mcp-Name`, and any `Mcp-Param-*` routing
  headers against the JSON-RPC body at gateway and origin.
- [ ] **SECURITY** Validate Host/Origin, proxy/forwarded headers, TLS boundary,
  body limits and deny-default egress.
- [ ] **SECURITY** Distributed user/tool/agent rate limits and fail behavior are
  implemented; agent identity comes from an authenticated policy, not metadata.

## Gates before data, jobs, or results

- [ ] JSON Schema 2020-12 contracts reject external `$ref`, unknown properties,
  ambiguous null/default/time/unit/numeric values, and schema resource exhaustion.
- [ ] Output schemas are server-validated; ordering, freshness, partial results,
  pagination snapshots and compatibility are explicit.
- [ ] Handles are high entropy, purpose-bound, re-authorized, revocable, expiring,
  quota-limited and backed by an approved shared/upstream/self-contained design.
- [ ] Cancellation, deadlines, retries, late results and task resumption are bound
  to the original actor and arguments and survive failures only as promised.
- [ ] Data entitlement, retention, residency, encryption, backup and deletion
  policies are enforced from a trusted authority.
- [ ] Security audit records are separate from telemetry and have documented
  durability, tamper evidence, outage behavior, access and retention.
- [ ] Threat, contract, property/fuzz, cross-tenant, load/soak, cancellation,
  failover, recovery and model-eval suites pass for the affected surface.

## Release gate

- [ ] Reproducible build, dependency license/audit, SBOM, provenance, signature,
  secret/source/image/IaC scans and non-root/read-only runtime evidence pass.
- [ ] SLO, capacity, cost, RTO/RPO, dashboards, alerts and accountable on-call are approved.
- [ ] Canary, compatibility, cache invalidation, rollback/kill switch, restore and
  incident playbooks are exercised against the exact candidate artifact.
- [ ] Remaining risks and deviations have accountable owners and unexpired review dates.

## Deviations

None accepted. Open checklist items are unfinished gates, not deviations.
