# ADR-0005: Data admission and market-data semantics

- Status: accepted as no-data for M1; blocks M2 until expanded and re-approved
- Date: 2026-09-13
- Owner: repository owner for M1; data and quant/domain owners required for M2

## Context and options

Structural parsing does not establish causal or financial fitness. Uploads and
immutable object references also have different trust and lifecycle boundaries.

## Decision and consequences

- M1 admits no caller or market datasets and retains no data artifacts. This is
  the complete M0 decision for the current walking-skeleton boundary.

- Prefer bounded Arrow IPC or Parquet as the first candidate interchange format;
  the choice remains open until parser behavior and Gambit/Polars compatibility are
  measured. CSV, ZIP, HDF5, pickle and executable notebook inputs are not admitted
  by default and require separate capability evidence.
- Distinguish controlled upload from immutable object registration. Both require an
  exact object version and digest; uploads additionally require quarantine and
  cleanup states. No arbitrary URL or filesystem path is accepted.
- Bind a versioned semantic profile to every admitted dataset: timestamp and
  publication-time meaning, timezone/DST, calendar/session, instrument identity,
  units/currency, adjustment/corporate-action policy, futures rolls, duplicates,
  ordering, missingness, revisions, and provenance.
- Report `well_formed` separately from `financially_qualified`. Only qualified
  datasets may enter a claimed-capability backtest.
- Entitlement metadata comes from a trusted administrative authority, not a model:
  owner/provider, license/purpose, region, expiry, derived-output and export policy.

## Verification and acceptance

M2 acceptance requires a final format decision, parser sandbox and hostile corpus
results, compressed/expanded
and schema budgets, admission state-machine tests, immutable-version/TOCTOU tests,
semantic golden cases across DST/sessions/revisions/adjustments/rolls, enforcement
of entitlements, and data plus quant-owner approval.
