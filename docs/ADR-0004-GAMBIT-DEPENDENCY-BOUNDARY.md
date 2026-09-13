# ADR-0004: Gambit dependency and capability boundary

- Status: accepted for M1; M2 artifact approval remains open
- Date: 2026-09-13
- Owner: repository owner for M1; Gambit/core and quant/domain owners required for M2

## Context and options

The reviewed Gambit commit is a beta research/backtesting library with supported,
experimental, and out-of-scope capabilities. Depending on a working-tree branch
would violate the production repository standard. Options are a published release,
an immutable source commit, or no dependency until an approved artifact exists.

## Decision and consequences

- M1 has no Gambit runtime dependency.
- M2 must pin an approved, immutable `gambit-markets` wheel/version with hashes and
  upstream release evidence. A commit-built artifact is allowed only with its own
  reproducible provenance; never depend on a moving branch or editable path.
- An owned `GambitPort` exposes only approved workflows and translates owned domain
  types at the boundary. MCP schemas never mirror the entire `gambit.__all__` API.
- Capability metadata preserves Gambit's supported/experimental status. Live
  trading remains out of scope.
- Every upgrade reruns adapter contracts, independent financial cases, security
  evidence for native/parser paths, performance checks, and compatibility review.

## Verification and acceptance

M0 accepts having no Gambit runtime dependency in M1. M2 acceptance requires the
exact artifact digest, license/native inventory, supported
platform matrix, public-API contract tests, independent validation golden cases,
feature-status mapping, rollback version, and Gambit plus quant-owner approval.
