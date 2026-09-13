# gambit-mcp Project Memory

This is a bounded retrieval index for durable project knowledge. It is not an
activity log, task tracker, transcript, or source of truth. Verify every entry
against the linked implementation, test, issue, or decision record before acting.

Do not record secrets, personal data, client data, hidden reasoning, or other
restricted material. Consult an existing key before editing and update it in
place. Remove stale entries and resolved work instead of preserving a narrative;
Git history provides the audit trail.

## Durable constraints

| Key | Constraint | Evidence | Last verified |
|---|---|---|---|
| `scope-read-only` | Initial service is read-only research: no live trading, arbitrary code, caller paths, or arbitrary URLs. | `PROJECT_BRIEF.md`, `docs/ADR-0001-BOUNDARY-AND-PROTOCOL.md` | 2026-09-13 |
| `remote-gate` | Streamable HTTP is localhost/pre-production only until the M3 authorization and network gates pass. | `docs/MCP_SERVER_ENGINEERING_STANDARD.md` | 2026-09-13 |

## Accepted decisions

| Key | Decision and rationale | Evidence | Last verified |
|---|---|---|---|
| `separate-service` | Keep MCP in `gambit-mcp`; access Gambit later through an owned adapter to its approved public artifact. | `docs/ADR-0001-BOUNDARY-AND-PROTOCOL.md` | 2026-09-13 |
| `protocol-baseline` | Target MCP 2026-07-28 with Python SDK 2.2.0; retain a tested legacy-era path until the host matrix is decided. | `docs/ADR-0001-BOUNDARY-AND-PROTOCOL.md`, `tests/test_mcp_server.py` | 2026-09-13 |
| `m0-boundary` | M0 is complete only for local stdio, static/no-data M1; ADR-0002 through ADR-0006 require new specialist approval before their later capability expansions. | `docs/M0_SIGNOFF.md` | 2026-09-13 |

## Non-obvious current state

| Key | State worth retrieving later | Evidence | Last verified |
|---|---|---|---|
| `m1-surface` | M1 exposes two static resources and one synthetic contract tool; it intentionally has no Gambit runtime dependency. | `src/gambit_mcp/server.py`, `docs/PROJECT_PLAN.md` | 2026-09-13 |
| `m1-complete` | M1 is complete only for the local/no-data boundary; limits, real stdio, Inspector, artifacts, audit and container smoke passed. | `docs/M1_SIGNOFF.md` | 2026-09-13 |

## Verified traps and failed approaches

| Key | Symptom and cause | Evidence or reproducer | Last verified |
|---|---|---|---|
| `standard-corrections` | The template MCP standard's Section 17 corrections must be applied; its earlier OAuth roles and stateless/shared-state wording are not copied literally. | `docs/MCP_SERVER_ENGINEERING_STANDARD.md` | 2026-09-13 |

## Open threads

| Key | Unresolved question or next evidence | Owner | Review by |
|---|---|---|---|
| `owners` | Repository owner covers M0/M1; named security, Gambit, quant/domain, data, operations and release owners remain required before affected later milestones. | Repository owner | 2026-09-20 |
| `capability-decisions` | Additional hosts, IdP/claims, Gambit artifact, first data format/profile, and queue/store/worker platform remain blocked at M2-M4, not M0. | UNASSIGNED | 2026-09-20 |
