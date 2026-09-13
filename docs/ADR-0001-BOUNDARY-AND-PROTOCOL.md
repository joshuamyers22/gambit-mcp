# ADR-0001: Separate read-only MCP service and protocol baseline

- Status: accepted for M0/M1; production approval remains separate
- Date: 2026-09-13
- Owner: repository owner

## Context and options

Gambit is a beta research/backtesting library with experimental capabilities and
native code. MCP transport, authorization and agent-facing schemas have different
dependencies, threat boundaries and release cadence. Options were embedding MCP
inside Gambit, a separate thin service, or postponing all implementation.

## Decision and consequences

Use a separate `gambit-mcp` repository and an owned adapter around the eventual
published Gambit API. Target MCP `2026-07-28` with Python SDK `2.2.0`. M1 supports
trusted stdio and localhost-only Streamable HTTP, contains no Gambit runtime
dependency or user data, and exposes only static resources plus a synthetic
read-only contract tool. The SDK's legacy era is tested until named clients allow
an explicit modern-only decision.

The service does not use self-reported protocol metadata as identity, hidden
transport sessions, deprecated protocol features, arbitrary code/path/URL input,
or live-trading capabilities. Protected remote HTTP is a later security gate.

## Verification

In-process modern and legacy clients must list exactly the intended surface, read
the safety profile and receive structured contract output. Reconsider when the
target host matrix, approved Gambit artifact, protocol revision or SDK major changes.
