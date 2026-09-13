# M1 latency and capacity budget

Status: proposed targets; shared-development-machine measurements are diagnostic,
not production acceptance evidence.

## Scope

- Paths: discovery, static resource reads, and `gambit_check_contract`.
- Boundary: request accepted by MCP HTTP/stdio transport through complete response.
- Deadline miss: fail without side effects; no partial financial result exists.
- Owner/review date: unassigned / 2026-09-20.
- Workload: current static M1 surface with no upstream calls or persisted state.

## Objectives

| Load | p50 | p95 | p99 | Throughput | Error limit |
|---|---:|---:|---:|---:|---:|
| Expected | TBD | <= 250 ms | TBD | TBD | < 0.1% server errors |
| Peak | TBD | TBD | TBD | TBD | < 1% server errors |
| Overload | N/A | N/A | N/A | reject above 8 in-flight calls | no unbounded queue |

## Bounds and failure behavior

- Request body: 1,048,576 bytes maximum.
- Structured response: 65,536 bytes maximum.
- Concurrent calls: 8 per process until distributed policy is selected.
- Tool wall time: 30 seconds.
- HTTP binds to loopback unless an approved deployment explicitly overrides it.
- M1 has no automatic retry, upstream deadline, application queue, or cache.
- Shutdown target: 30 seconds; unfinished read-only work may be cancelled.

## Required evidence

- Enforce every configured limit at the real transport/handler boundary.
- Measure p50/p95/p99, throughput, RSS, CPU and errors at expected, peak and
  overload on declared production-like hardware.
- Verify deterministic response bytes and no stdout corruption over stdio.
- Retain command, workload revision, environment and raw aggregate artifact.
- Reject promotion if memory/in-flight work grows without bound or overload is
  queued silently.
