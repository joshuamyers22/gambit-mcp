# M0 decisions and contracts signoff

- Status: complete for the local, read-only M1 boundary
- Date: 2026-09-13
- Accountable role: repository owner
- Production approval: not granted

## Scope accepted

M0 authorizes development of the M1 walking skeleton through trusted local stdio.
MCP Python SDK Client 2.2.0 is the supported host, using the target
`2026-07-28` revision; its `2025-11-25` compatibility path remains tested. The
loopback HTTP server is development/conformance-only and is not a supported remote
deployment.

M1 admits no market or user data, has no Gambit runtime dependency, application
handles, durable state, worker, artifact store, remote identity provider, write
operation, live trading, arbitrary code, caller path, or arbitrary URL.

## Evidence reviewed

| M0 requirement | Decision/evidence | Disposition |
|---|---|---|
| Project boundary and invariants | `PROJECT_BRIEF.md`, ADR-0001 | Accepted for M1 |
| Protocol and transport | ADR-0001, ADR-0002, `uv.lock` | Accepted for M1 |
| Authorization boundary | ADR-0003 | Local-launcher trust accepted; remote auth deferred to M3 |
| Gambit dependency | ADR-0004 | No dependency accepted; artifact approval gates M2 |
| Data semantics/admission | ADR-0005 | No-data boundary accepted; format/profile gates M2 |
| State and isolation | ADR-0006 | Stateless/no-worker boundary accepted; platform gates M4/M5 |
| Threat model | `THREAT_MODEL.md` | Accepted only for current local/no-data surface |
| Capacity targets | `LATENCY_BUDGET_M1.md` | Proposed M1 verification targets accepted |
| Traceability | `REQUIREMENTS_TRACEABILITY.md` | Established; downstream evidence remains open |

## Explicitly deferred decisions

These are capability gates, not M0 defects: additional MCP hosts; remote HTTP and
IdP; an immutable Gambit artifact; market-data format and semantic profile;
entitlement authority; queue/store/worker platform; production SLO/RPO/RTO; and
named security, domain, data, operations and release approvers.

No later milestone may infer those decisions from this signoff. The corresponding
ADR must be expanded, re-reviewed, and accepted by its named specialist owner.

## M1 entry criteria

- The initial surface stays static, bounded, read-only and no-data.
- Every change maps to `REQUIREMENTS_TRACEABILITY.md`.
- M1 must still prove real stdio integrity, enforced limits, golden-wire behavior,
  dependency/license checks, and client evaluation before it can close.
