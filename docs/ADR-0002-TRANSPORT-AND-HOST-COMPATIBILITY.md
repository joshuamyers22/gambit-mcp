# ADR-0002: Transport and host compatibility

- Status: accepted for M1
- Date: 2026-09-13
- Owner: repository owner

## Context and options

The server needs a trusted local mode and may later need protected remote access.
MCP `2026-07-28` is stateless, while older clients use initialization-era
semantics. Options are modern-only, dual-era compatibility, or separate endpoints.

## Decision and consequences

- Support stdio with MCP Python SDK Client 2.2.0 as the initial client/host matrix.
  Qualify the modern `2026-07-28` path and retain the SDK's `2025-11-25` legacy
  path as compatibility evidence. Other hosts are unsupported until added by test.
- Allow Streamable HTTP only on loopback for development and conformance testing.
  It is not a supported deployed mode in M1.
- Do not implement legacy HTTP+SSE.
- Target `2026-07-28`. Temporarily test the SDK's `2025-11-25` compatibility path
  until named target hosts are inventoried; this is not a promise of indefinite
  dual-era support.
- Use no transport-session affinity. Any future cross-call state must resolve via
  shared durable state, upstream-owned state, or a separately reviewed sealed handle.
- Bind HTTP to loopback by default. Remote exposure requires M3 authorization,
  Host/Origin and header/body parity controls, TLS/proxy policy, and negative tests.

## Verification and acceptance

M0 acceptance is the explicit matrix and transport boundary above. M1 completion
requires modern and legacy golden-wire tests, stdio corruption testing, and a
documented rejection response for unsupported revisions. Round-robin HTTP evidence
belongs to M3 before deployed HTTP. Reconsider on a protocol revision, SDK major,
or proposed host change.
