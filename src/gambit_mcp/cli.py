"""MCP process entry point."""

from __future__ import annotations

from .server import build_server
from .settings import Settings


def main() -> int:
    settings = Settings()
    server = build_server(settings)
    if settings.transport == "stdio":
        server.run(transport="stdio")
    else:
        server.run(
            transport="streamable-http",
            host=settings.host,
            port=settings.port,
            streamable_http_path=settings.mcp_path,
            stateless_http=True,
            max_request_body_size=settings.max_request_body_bytes,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
