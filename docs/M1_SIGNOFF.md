# M1 walking-skeleton sign-off

Status: complete for the approved local, read-only, no-data boundary on
2026-09-13. This is not remote-deployment or production approval.

## Delivered surface

- Two deterministic JSON resources: `gambit://server/about` and
  `gambit://capabilities`.
- One typed synthetic tool: `gambit_check_contract`.
- MCP Python SDK 2.2.0 with target protocol 2026-07-28 and tested legacy-era
  compatibility.
- Trusted local stdio and loopback-only Streamable HTTP for development and
  conformance.
- No Gambit runtime, user or market data, persistence, jobs, remote identity,
  arbitrary code/path/URL access, or trading behavior.

## Exit evidence

| Gate | Evidence | Result |
|---|---|---|
| Typed discovery, tool and resource contracts | `tests/test_mcp_server.py` | Pass |
| Modern metadata and legacy negotiation | in-process and real-process SDK tests | Pass |
| Stdio protocol integrity | debug-logging subprocess remains parseable by a real MCP client | Pass |
| Request, response, concurrency and tool-time bounds | `src/gambit_mcp/limits.py`, `tests/test_limits.py` | Pass |
| HTTP frame bound | SDK body-limit integration test returns 413 before dispatch | Pass |
| Independent client interoperability | official MCP Inspector CLI strict tools/list, tools/call and resources/read | Pass |
| Code quality | Ruff, format, Pyright strict, 17 tests | Pass |
| Frozen artifact | lock check, release metadata check, wheel and sdist build | Pass |
| Production dependency audit | `uv audit --locked --no-dev` | No known vulnerabilities/adverse statuses |
| Container contract | immutable-base build and real-socket non-root smoke | Pass |

Inspector commands used:

```sh
npx --yes @modelcontextprotocol/inspector --cli uv run gambit-mcp --transport stdio --method tools/list --strict --format json --cwd "$PWD"
npx --yes @modelcontextprotocol/inspector --cli uv run gambit-mcp --transport stdio --method tools/call --tool-name gambit_check_contract --tool-args-json '{"contract_version":"v1"}' --format json --cwd "$PWD"
npx --yes @modelcontextprotocol/inspector --cli uv run gambit-mcp --transport stdio --method resources/read --uri gambit://server/about --format json --cwd "$PWD"
```

## Explicitly deferred gates

- Streamable HTTP `Mcp-*` header/body parity, remote authentication,
  authorization, tenant isolation, and distributed rate limits remain M3 gates.
- Market-data semantics, Gambit correctness, parser hardening, and domain golden
  cases remain M2 or later gates.
- Model task evaluations, production-like load/soak evidence, SBOM, provenance,
  signing, canary and rollback exercises remain M6 production-promotion gates.
- Additional named clients or hosts require evidence under ADR-0002.

The repository owner accepts this narrow M1 result. Any expansion requires the
ADR approvals and evidence assigned to its later milestone.
