# Release Readiness

- [ ] Critical journeys, invariants, and failure paths have evidence.
- [ ] Dependencies are locked, audited, and licensed appropriately.
- [ ] The semantic-version tag exactly matches project metadata.
- [ ] Build artifacts, OCI digest, revision, and SBOM are traceable to the commit.
- [ ] The published digest has attached SBOM/provenance and no `latest` tag.
- [ ] Secrets and private data are absent from source, artifacts, health data, and logs.
- [ ] `PROJECT_MEMORY.md` is evidence-linked, deduplicated, current, and contains
      no secrets, private data, hidden reasoning, or restricted material.
- [ ] Tracked work notes are closed or current and contain no raw telemetry.
- [ ] Material agent-assisted changes have requirement-linked evidence, bounded
      iteration/resource ceilings, explicit stop rules, and accountable approval;
      token or iteration counts alone are not treated as quality evidence.
- [ ] Threats, migrations, compatibility, rollback, and recovery were reviewed.
- [ ] SLI/SLOs, alerts, dashboards, capacity, and operational ownership are adequate.
- [ ] Applicable latency budgets have production-like percentile, overload,
      replay, and regression evidence.
- [ ] The identical candidate digest passed the prior environment.
- [ ] Remote deployment verification passed for the expected environment and revision.
- [ ] Rollback commands and one dependency-failure response were exercised.
- [ ] Termination grace exceeds application shutdown plus routing drain time.
- [ ] Remaining risks have owners and dates.
- [ ] Events/errors conform to the versioned schema; telemetry review links
      reproducible aggregates to an owned, guarded improvement decision.
