# Requirements traceability

Status: M0 baseline accepted for the local/no-data M1 boundary. `Open` means the
requirement remains for its named milestone; it does not reopen M0 unless the M1
boundary changes.

| ID | Requirement | Source | Verification | Gate | Status |
|---|---|---|---|---|---|
| R-001 | Separate MCP transport from Gambit | Plan invariant | ADR-0001 and package boundary review | M0 | Accepted |
| R-002 | Target MCP 2026-07-28 with a pinned Tier 1 SDK | MCP standard | Lockfile and modern client contract | M1 | Implemented |
| R-003 | Define supported host/protocol matrix | MCP standard | ADR-0002 plus SDK client contracts | M0/M1 | M0 accepted; M1 wire evidence open |
| R-004 | No live trading, arbitrary code/path/URL, or investment advice | Project brief | Surface inventory and negative schema tests | All | Partially implemented |
| R-005 | Transport-specific identity and authorization | MCP standard | ADR-0003 and authorization matrix | M0/M3 | Local M1 accepted; M3 open |
| R-006 | Preserve Gambit maturity/capability labels | Gambit brief/status | Capability projection contract tests | M2+ | Proposed |
| R-007 | Pin an approved immutable Gambit artifact | Production standard | Artifact digest, lockfile and upstream evidence | M2 | No dependency in M1; M2 open |
| R-008 | Bound every request, response, call and queue | MCP standard | Boundary and saturation tests | M1+ | Configured; enforcement open |
| R-009 | Admit only explicit formats through a parser trust boundary | GAP-01 | Hostile corpus and admission-state tests | M2 | Proposed |
| R-010 | Version causal market-data semantics | GAP-02 | Quant/data golden and rejection cases | M2/M5 | Proposed |
| R-011 | Enforce trusted data entitlements | GAP-03 | Policy transition/enforcement matrix | M4 | Proposed |
| R-012 | Define byte and financial replay levels | GAP-04 | Same/cross-host replay and invalidation | M5 | Open |
| R-013 | Explicit durable job authorization and revocation | GAP-05 | Job-state authorization race matrix | M4 | Proposed |
| R-014 | Separate durable audit from telemetry | GAP-06 | Sink/spool/tamper/restore tests | M3/M4 | Proposed |
| R-015 | Encrypt and precisely delete every data copy class | GAP-07/GAP-14 | Key and deletion/restore drills | M4 | Proposed |
| R-016 | Quarantine and supersede affected results | GAP-08 | Synthetic correction drill | M4 | Proposed |
| R-017 | Bound declarative strategies by registry and cost | GAP-09 | Adversarial estimate/observed corpus | M5 | Open |
| R-018 | Snapshot-bind pagination | GAP-10 | Concurrent mutation/cursor tests | M4 | Open |
| R-019 | Separate disconnect and cancellation semantics | GAP-11 | Lifecycle race matrix | M4 | Proposed |
| R-020 | Fair multi-tenant scheduling and budgets | GAP-12 | Fairness/retry-storm reconciliation | M6 | Open |
| R-021 | Version capabilities across rolling deployments | GAP-13 | Contract digest and N/N-1 tests | M6 | Open |
| R-022 | Produce privacy-safe structured telemetry | Template/MCP standard | Schema and redaction tests | M1+ | Partially implemented |
| R-023 | Reproducible secure artifact and rollback | Production standard | Clean build, SBOM/provenance, scans and drill | M6 | Partially implemented |
