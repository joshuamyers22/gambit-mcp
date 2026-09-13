"""MCP composition root for the bounded walking skeleton."""

from __future__ import annotations

import json
import re
import uuid
from typing import Literal

from mcp.server import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse

from .contracts import CapabilityProfile, ContractCheck, ServerProfile
from .logging import configure_logging
from .settings import Settings

REQUEST_ID = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


def _request_id(request: Request) -> str:
    supplied = request.headers.get("x-request-id", "")
    return supplied if REQUEST_ID.fullmatch(supplied) else uuid.uuid4().hex


def build_server(settings: Settings | None = None) -> MCPServer:
    """Build a server with no implicit cross-request state."""

    config = settings or Settings()
    configure_logging(
        config.log_level,
        service="gambit-mcp",
        environment=config.environment,
        release=config.release,
        revision=config.revision,
    )
    server = MCPServer(
        "gambit-mcp",
        version="0.1.0",
        instructions=(
            "Read-only research server. It does not trade, execute uploaded code, "
            "or currently run Gambit calculations."
        ),
    )

    @server.resource("gambit://server/about", mime_type="application/json")
    def about() -> str:  # pyright: ignore[reportUnusedFunction]
        """Return server identity, maturity, and non-trading safety boundary."""

        return json.dumps(ServerProfile().model_dump(), sort_keys=True)

    @server.resource("gambit://capabilities", mime_type="application/json")
    def capabilities() -> str:  # pyright: ignore[reportUnusedFunction]
        """Return implemented and explicitly unavailable capabilities."""

        return json.dumps(CapabilityProfile().model_dump(), sort_keys=True)

    @server.tool(title="Check Gambit MCP contract")
    def gambit_check_contract(  # pyright: ignore[reportUnusedFunction]
        contract_version: Literal["v1"],
    ) -> ContractCheck:
        """Check compatibility with the walking-skeleton contract.

        Use this before relying on this pre-production server. It validates only
        the MCP adapter contract. It does not validate data, run Gambit, backtest,
        calculate risk, or provide investment advice.
        """

        return ContractCheck(contract_version=contract_version)

    @server.custom_route("/health/live", methods=["GET"], include_in_schema=False)
    async def live(  # pyright: ignore[reportUnusedFunction]
        request: Request,
    ) -> JSONResponse:
        """Return process liveness without configuration or dependency details."""

        return JSONResponse(
            {"status": "ok"}, headers={"x-request-id": _request_id(request)}
        )

    @server.custom_route("/health/ready", methods=["GET"], include_in_schema=False)
    async def ready(  # pyright: ignore[reportUnusedFunction]
        request: Request,
    ) -> JSONResponse:
        """Return M1 readiness; no upstream dependencies exist yet."""

        return JSONResponse(
            {"status": "ready"}, headers={"x-request-id": _request_id(request)}
        )

    @server.custom_route("/health/version", methods=["GET"], include_in_schema=False)
    async def version(  # pyright: ignore[reportUnusedFunction]
        request: Request,
    ) -> JSONResponse:
        """Return traceable release identity without sensitive configuration."""

        return JSONResponse(
            {
                "service": "gambit-mcp",
                "environment": config.environment,
                "release": config.release,
                "revision": config.revision,
            },
            headers={"x-request-id": _request_id(request)},
        )

    return server
