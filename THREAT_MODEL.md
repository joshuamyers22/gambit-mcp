# Threat model

Status: reviewed and accepted by the repository owner for the local, no-data M1
boundary on 2026-09-13. Independent security/domain approval is required before
remote access, Gambit execution, data admission, or production promotion.

## Boundary

M1 processes MCP protocol traffic and returns static project-owned metadata. It
does not accept market data, persist application state, call Gambit, fetch remote
content, or execute user code. Stdio trusts the launching user/process. HTTP binds
to localhost and is not approved for remote production.

## Assets, actors, and flows

- Assets: source and release identity, tool/resource contracts, configuration,
  telemetry, process CPU/memory, and future confidential market data/results.
- M1 actors: local launching user/process, MCP host/client, repository contributor,
  dependency publisher, build/release operator. Remote users and tenants are not
  admitted yet.
- Trust flow: client protocol bytes enter the SDK transport, validated arguments
  enter project handlers, static project-owned results return through SDK output
  serialization, and diagnostics go to stderr. No M1 upstream or persistence flow exists.
- Future boundaries requiring a new review: OAuth ingress, data admission/parser,
  Gambit/native worker, queue/state store, artifact storage, audit sink and exports.

## Threats and current controls

| Threat | M1 control | Residual/open work |
|---|---|---|
| Malformed/oversized protocol input | SDK schemas; configured size ceiling | Transport enforcement and fuzz evidence open |
| Tool-description or result poisoning | Static reviewed source; no upstream text | Dependency integrity and eval review required |
| Stdio protocol corruption | Diagnostics configured on stderr | Captured-wire regression still required |
| Local-network/DNS rebinding access | Loopback default; SDK transport security defaults | Host/Origin/proxy tests required before HTTP promotion |
| Identity or tenant confusion | No M1 tenant data or protected remote deployment | Full principal/auth matrix blocks M3 |
| Resource exhaustion | Small static surface and numeric configuration bounds | Enforcement, concurrency and load evidence open |
| Supply-chain compromise | Exact MCP/runtime pins planned in lockfile | Audit, SBOM, provenance and scans required |
| Misleading financial claim | No financial tools; machine-readable non-trading boundary | Independent evidence required before M2/M5 |
| Header/body authorization disagreement | No protected gateway in M1 | Exact parity enforcement at gateway and origin blocks M3 |
| Confused deputy or forged client metadata | M1 does not use metadata as authority | Authenticated principal model and negative tests block M3 |
| Stale/guessed application handle | No handles in M1 | Handle lifecycle and per-use authorization block M4 |

## Approval

No residual risk is accepted for production. Review again before any Gambit
dependency, user data, durable state, remote exposure, or new tool/resource.
