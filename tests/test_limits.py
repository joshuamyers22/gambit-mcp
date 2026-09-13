from unittest import IsolatedAsyncioTestCase

import anyio
from mcp.shared.exceptions import MCPError

from gambit_mcp.limits import (
    DEADLINE_EXCEEDED,
    LIMIT_EXCEEDED,
    SERVER_BUSY,
    BoundaryLimits,
)


class _Context:
    method = "tools/call"
    params: dict[str, object] = {}


class BoundaryLimitsTests(IsolatedAsyncioTestCase):
    async def test_rejects_oversized_request(self) -> None:
        limits = BoundaryLimits(
            max_request_bytes=32,
            max_response_bytes=1024,
            max_concurrent_calls=1,
            tool_timeout_seconds=1,
        )
        context = _Context()
        context.params = {"value": "x" * 64}

        with self.assertRaises(MCPError) as raised:
            await limits(context, lambda _: anyio.sleep(0))  # type: ignore[arg-type]
        self.assertEqual(raised.exception.error.code, LIMIT_EXCEEDED)

    async def test_rejects_oversized_response(self) -> None:
        limits = BoundaryLimits(
            max_request_bytes=1024,
            max_response_bytes=32,
            max_concurrent_calls=1,
            tool_timeout_seconds=1,
        )

        async def large_response(_: object) -> dict[str, str]:
            return {"value": "x" * 64}

        with self.assertRaises(MCPError) as raised:
            await limits(_Context(), large_response)  # type: ignore[arg-type]
        self.assertEqual(raised.exception.error.code, LIMIT_EXCEEDED)

    async def test_tool_deadline_is_enforced(self) -> None:
        limits = BoundaryLimits(
            max_request_bytes=1024,
            max_response_bytes=1024,
            max_concurrent_calls=1,
            tool_timeout_seconds=0.01,
        )

        async def slow_response(_: object) -> None:
            await anyio.sleep(1)

        with self.assertRaises(MCPError) as raised:
            await limits(_Context(), slow_response)  # type: ignore[arg-type]
        self.assertEqual(raised.exception.error.code, DEADLINE_EXCEEDED)

    async def test_concurrency_limit_fails_fast(self) -> None:
        limits = BoundaryLimits(
            max_request_bytes=1024,
            max_response_bytes=1024,
            max_concurrent_calls=1,
            tool_timeout_seconds=1,
        )
        entered = anyio.Event()
        release = anyio.Event()

        async def blocked(_: object) -> None:
            entered.set()
            await release.wait()

        async with anyio.create_task_group() as tasks:
            tasks.start_soon(limits, _Context(), blocked)  # type: ignore[arg-type]
            await entered.wait()
            with self.assertRaises(MCPError) as raised:
                await limits(_Context(), blocked)  # type: ignore[arg-type]
            self.assertEqual(raised.exception.error.code, SERVER_BUSY)
            release.set()
