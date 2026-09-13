# M2 market-data validation readiness

Status: implementation groundwork started; public capability remains blocked.

## Verified upstream state

- Reviewed Gambit commit: `9c550bdae592e975f12046ebbb8d690889fd9206`.
- Declared upstream package/version: `gambit-markets` 1.1.0, BSD-3-Clause.
- Stable public function at the reviewed commit: `gambit.validate_market_data`.
- Artifact check on 2026-09-13: no PyPI project, GitHub release, or Git tag was
  available. The working branch is not an admissible dependency artifact.

## Implemented groundwork

- `MarketDataBatch` is an owned, parser-independent normalized boundary.
- Profile version, instrument, currency, calendar, adjustment policy, row count,
  timezone awareness, price/volume finiteness, and strict timestamp ordering are
  fail-closed before any future Gambit adapter call.
- `MarketDataValidation` separates `well_formed` from
  `financially_qualified` and bounds returned findings.
- `GambitPort` exposes only market-data validation rather than Gambit's full API.
- No MCP tool, binary parser, Gambit dependency, persistence, path, URL, or remote
  capability has been added.

## Blocking decisions and evidence

1. Gambit/core owner must publish and approve an immutable wheel with hashes,
   provenance, platform matrix, license/native inventory, and rollback version.
2. Data and quant/domain owners must approve semantic profile v1: timestamp and
   availability meaning, timezone/DST, calendar/session policy, instrument
   identity, units/currency, adjustments, duplicates, ordering, missingness,
   revisions, provenance, and qualification rules.
3. Choose one bounded ingestion mode. Arrow IPC remains the leading candidate;
   Parquet requires separate compressed/expanded limits. Neither is exposed yet.
4. Define parser isolation, byte/row/column/metadata/time/memory limits and run a
   hostile corpus before parsing caller bytes.
5. Add independent golden cases for DST, sessions, revisions, adjustments and
   rolls. Repository-authored cases are regression tests, not domain approval.

Until all five gates pass, M2 remains in progress and `gambit_check_contract`
remains the only tool.
