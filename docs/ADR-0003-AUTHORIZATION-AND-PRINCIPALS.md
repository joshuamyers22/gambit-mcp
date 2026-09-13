# ADR-0003: Authorization and principal model

- Status: accepted for M1 local-only boundary; M3 expansion requires a new approval
- Date: 2026-09-13
- Owner: repository owner for M1; security/identity owner required for M3

## Context and roles

M1 stdio exposes no user data and trusts the launching OS user/process. A future
remote deployment makes `gambit-mcp` an OAuth resource server; it is not the OAuth
client or authorization server. Self-reported MCP `clientInfo` identifies software
for diagnostics only and cannot establish a user, tenant, or agent identity.

## Decision and consequences

- M1 supports only local stdio under the launching OS user's authority. It does
  not add a second application identity, accept user data, or claim tenant isolation.
- M1 loopback HTTP is unauthenticated development-only and must not be exposed or
  described as a supported deployment.

- Define principals separately: human user, tenant, client application,
  authenticated agent/workload, and server service identity.
- Use an approved external identity provider. Publish RFC 9728 Protected Resource
  Metadata and issue correct `WWW-Authenticate` challenges.
- Validate token signature, issuer, audience/resource, expiry, not-before,
  algorithm, tenant claim, and scopes on every protected HTTP operation.
- Begin with `gambit:read` and `gambit:validate`; defer `gambit:run` until jobs are
  approved. Keep administrative operations outside the model-facing server.
- Re-authorize every handle/resource use. Possession of a handle is never authority.
- Do not pass caller tokens into Gambit or another upstream system.

## Verification and acceptance

M0 accepts the no-remote-auth M1 boundary. M3 acceptance requires the named IdP,
canonical resource URI, claim contract, scope/
object matrix, JWKS refresh and outage policy, clock skew, revocation behavior,
cross-tenant tests, and transitions for queued/running work. Failure defaults closed
for protected operations. Exact degraded behavior must be approved per dependency.
