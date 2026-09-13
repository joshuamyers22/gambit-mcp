# Deployment contract

This service is deployable to any platform that runs the OCI image and provides
HTTPS ingress. Selecting a provider, registry, region, network boundary, scaling
policy, persistence layer, and secret store remains a project decision recorded
in an ADR. Do not call the service production-ready while those items remain
unresolved in `PROJECT_BRIEF.md`.

## Artifact identity

Build once and promote the same image digest through environments. Never rebuild
for promotion and never deploy a mutable tag such as `latest`.

```sh
make container APP_RELEASE=1.2.3 APP_REVISION=<full-commit-sha>
docker inspect gambit-mcp:local \
  --format '{{index .Config.Labels "org.opencontainers.image.revision"}}'
```

The image exposes its release, revision, service, and runtime environment at
`/health/version`. Production startup fails when `APP_REVISION` is `local` or
`unknown`. Set `APP_ENVIRONMENT` at deployment time; it is environment state,
not an image property.

## Registry publication and provenance

A version tag that exactly matches `pyproject.toml` (for example, `v1.2.3`)
publishes a Linux AMD64/ARM64 image to
`ghcr.io/<owner>/<repository>`. The workflow emits only the exact semantic
version and full commit-SHA tags; it explicitly disables `latest`. BuildKit
attaches an image SBOM and maximal provenance, and the GitHub release records the
immutable `name@sha256:digest` in `image-digest.txt`.

Deployment automation must consume that digest, not either tag. Keep the digest
for every active deployment and at least one tested rollback candidate. Define
untagged-image retention and legal/audit retention before production; garbage
collection must not delete a referenced rollback digest.

GitHub-native signed artifact attestations for private repositories require an
Enterprise Cloud plan. Public Sigstore transparency logging can disclose private
repository identity. This baseline therefore records BuildKit provenance but
does not claim cryptographic publisher verification. Record an ADR before
enabling GitHub attestations, public keyless signing, or private key/KMS signing.


## Promotion gates

For each environment, record the image digest, release, revision, configuration
version, approver, start time, and result.

1. Confirm CI, dependency audit, secret scan, artifact SBOM, and change approval.
2. Confirm the candidate digest is the digest tested in the prior environment.
3. Confirm backward/forward compatibility and migration ordering.
4. Deploy to a non-production environment and wait for platform health checks.
5. Run the remote verification command below.
6. Review errors, latency, saturation, dependency health, and critical journey
   signals for the project's documented observation window.
7. Promote the identical digest with an explicit production approval.
8. Repeat verification and record the evidence.

```sh
make deployment-smoke \
  BASE_URL=https://service.example.com \
  EXPECTED_ENVIRONMENT=production \
  EXPECTED_RELEASE=1.2.3 \
  EXPECTED_REVISION=<full-commit-sha>
```

The verifier requires a credential-free HTTPS origin, refuses redirects, checks
liveness and readiness, verifies request-ID propagation, and proves the running
artifact identity. It covers deployment wiring, not authenticated business
journeys; add project-specific post-deployment probes that use synthetic,
non-sensitive accounts.

## Rollback and migrations

Before the first production deployment, replace the placeholders below with
tested platform commands and name the operator:

- Deployment owner and backup: TODO
- Pause/abort rollout command: TODO
- Restore prior image digest command: TODO
- Verify restored revision command: use `make deployment-smoke`
- Escalation channel and incident commander: TODO
- Maximum rollback decision time: TODO

Rollback on elevated user-impacting errors, failed critical journeys, persistent
readiness failure, or an identity mismatch. Preserve the failed revision and
telemetry for analysis.

Database changes must use expand/migrate/contract sequencing. Deploy additive
schema changes before code that needs them; backfill with restartable,
observable jobs; remove old fields only after all old application revisions are
gone. If a migration is not backward compatible, document why rollback remains
safe or use a forward-fix plan approved before deployment.

## Health and shutdown contract

- `/health/live` proves the process can serve requests; do not add dependency
  checks that cause restart storms.
- `/health/ready` controls traffic admission. Add bounded checks when the
  service acquires dependencies required to serve requests.
- `/health/version` proves artifact and environment identity and must not expose
  secrets or host details.
- The platform termination grace period must exceed
  `APP_GRACEFUL_SHUTDOWN_SECONDS` plus its own routing-drain allowance.

## Observability and recovery

Every log line carries schema version, service, environment, release, revision,
UTC timestamp, severity, event, operation, and outcome. Request logs add a safe
correlation ID, route template, method, status, and duration. An unhandled error
adds the stable `UNHANDLED_REQUEST_ERROR` code, exception type, and retryability
without exposing its message. Do not log credentials, tokens, request bodies,
raw URLs, or personal data. Review aggregate events with
`templates/TELEMETRY_REVIEW.md` before proposing an owned improvement.

Before production, define user-centered SLIs/SLOs, paging thresholds, dashboard
links, retention, capacity limits, dependency alerts, and recovery objectives in
`PROJECT_BRIEF.md`. Exercise rollback and one dependency-failure scenario, then
record evidence in the release checklist. A green health endpoint alone is not
production evidence.
