"""Fail-closed request execution limits shared by every MCP transport."""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

import anyio
from mcp.server.context import HandlerResult, ServerRequestContext
from mcp.shared.exceptions import MCPError
from pydantic import BaseModel

LIMIT_EXCEEDED = -32001
SERVER_BUSY = -32002
DEADLINE_EXCEEDED = -32003


def _json_size(value: object) -> int:
    if isinstance(value, BaseModel):
        value = value.model_dump(by_alias=True, mode="json", exclude_none=True)
    return len(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    )


class BoundaryLimits:
    """Bound input, in-flight work, tool duration, and serialized output.

    HTTP frame size is additionally rejected by the SDK transport before JSON
    parsing. This middleware supplies equivalent method/params and execution
    bounds for stdio and in-process transports.
    """

    def __init__(
        self,
        *,
        max_request_bytes: int,
        max_response_bytes: int,
        max_concurrent_calls: int,
        tool_timeout_seconds: float,
    ) -> None:
        self._max_request_bytes = max_request_bytes
        self._max_response_bytes = max_response_bytes
        self._tool_timeout_seconds = tool_timeout_seconds
        self._capacity = anyio.CapacityLimiter(max_concurrent_calls)

    async def __call__(
        self,
        ctx: ServerRequestContext[Any, Any],
        call_next: Callable[[ServerRequestContext[Any, Any]], Awaitable[HandlerResult]],
    ) -> HandlerResult:
        request: Mapping[str, object] = {
            "method": ctx.method,
            "params": ctx.params,
        }
        if _json_size(request) > self._max_request_bytes:
            raise MCPError(LIMIT_EXCEEDED, "request exceeds configured size limit")

        try:
            self._capacity.acquire_nowait()
        except anyio.WouldBlock as error:
            raise MCPError(SERVER_BUSY, "server concurrency limit reached") from error

        try:
            try:
                if ctx.method == "tools/call":
                    with anyio.fail_after(self._tool_timeout_seconds):
                        result = await call_next(ctx)
                else:
                    result = await call_next(ctx)
            except TimeoutError as error:
                raise MCPError(DEADLINE_EXCEEDED, "tool deadline exceeded") from error

            if _json_size(result) > self._max_response_bytes:
                raise MCPError(LIMIT_EXCEEDED, "response exceeds configured size limit")
            return result
        finally:
            self._capacity.release()
