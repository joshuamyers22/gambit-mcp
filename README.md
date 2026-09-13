# gambit-mcp

Pre-production MCP server for bounded, read-only Gambit quantitative-research
workflows. The target protocol revision is `2026-07-28`; MCP Python SDK `2.2.0`
also serves the tested `2025-11-25` legacy era.

```sh
make setup
make check
uv run gambit-mcp
```

Current scope is only the M1 walking skeleton:

- `gambit://server/about` and `gambit://capabilities` resources;
- `gambit_check_contract`, a synthetic schema/compatibility tool;
- no market data, Gambit calculations, persistence, remote authorization, live
  trading, arbitrary code, filesystem paths, or arbitrary network access.

Set `APP_TRANSPORT=streamable-http` to run the pre-production HTTP transport on
localhost. It is not approved for remote production use.

Configuration uses `APP_` environment variables documented in `.env.example`.
Production refuses to start with an untraceable revision. The inherited HTTP
health and container deployment contract must be adapted and requalified for the
MCP ASGI app before container promotion. See `PROJECT_BRIEF.md`,
`docs/PROJECT_PLAN.md`, and `docs/MCP_SERVER_ENGINEERING_STANDARD.md`.
