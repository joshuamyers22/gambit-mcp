import json
import os
import sys
from unittest import IsolatedAsyncioTestCase, TestCase

from mcp import Client, StdioServerParameters
from mcp.types import TextResourceContents
from starlette.testclient import TestClient

from gambit_mcp.contracts import SPEC_REVISION
from gambit_mcp.server import build_server
from gambit_mcp.settings import Settings


class MCPServerContractTests(IsolatedAsyncioTestCase):
    async def test_modern_client_discovers_bounded_surface(self) -> None:
        server = build_server(Settings(environment="test"))
        async with Client(server, mode=SPEC_REVISION) as client:
            tools = await client.list_tools()
            resources = await client.list_resources()

        self.assertEqual([tool.name for tool in tools.tools], ["gambit_check_contract"])
        self.assertEqual(
            [str(resource.uri) for resource in resources.resources],
            ["gambit://server/about", "gambit://capabilities"],
        )

    async def test_real_stdio_process_has_clean_protocol_output(self) -> None:
        environment = os.environ.copy()
        environment.update(
            APP_ENVIRONMENT="test",
            APP_LOG_LEVEL="debug",
            APP_REVISION="stdio-test",
        )
        parameters = StdioServerParameters(
            command=sys.executable,
            args=["-m", "gambit_mcp.cli"],
            env=environment,
        )
        async with Client(parameters, mode="auto") as client:
            result = await client.call_tool(
                "gambit_check_contract", {"contract_version": "v1"}
            )
            protocol_version = client.protocol_version
            server_info = client.server_info

        self.assertFalse(result.is_error)
        self.assertEqual(protocol_version, SPEC_REVISION)
        self.assertIsNotNone(server_info)
        assert server_info is not None
        self.assertEqual(server_info.name, "gambit-mcp")
        self.assertEqual(server_info.version, "0.1.0")

    async def test_real_stdio_accepts_modern_protocol_metadata(self) -> None:
        environment = os.environ.copy()
        environment.update(APP_ENVIRONMENT="test", APP_REVISION="modern-wire-test")
        parameters = StdioServerParameters(
            command=sys.executable,
            args=["-m", "gambit_mcp.cli"],
            env=environment,
        )
        async with Client(parameters, mode=SPEC_REVISION) as client:
            result = await client.call_tool(
                "gambit_check_contract", {"contract_version": "v1"}
            )

        self.assertFalse(result.is_error)
        self.assertEqual(
            result.structured_content["target_spec_revision"], SPEC_REVISION
        )

    async def test_contract_tool_has_structured_bounded_output(self) -> None:
        server = build_server(Settings(environment="test"))
        async with Client(server, mode=SPEC_REVISION) as client:
            result = await client.call_tool(
                "gambit_check_contract", {"contract_version": "v1"}
            )

        self.assertFalse(result.is_error)
        self.assertEqual(
            result.structured_content,
            {
                "accepted": True,
                "contract_version": "v1",
                "scope": "read-only-research",
                "server_version": "0.1.0",
                "target_spec_revision": SPEC_REVISION,
            },
        )

    async def test_about_resource_exposes_safety_boundary(self) -> None:
        server = build_server(Settings(environment="test"))
        async with Client(server, mode=SPEC_REVISION) as client:
            result = await client.read_resource("gambit://server/about")

        content = result.contents[0]
        self.assertIsInstance(content, TextResourceContents)
        assert isinstance(content, TextResourceContents)
        profile = json.loads(content.text)
        self.assertEqual(profile["target_spec_revision"], SPEC_REVISION)
        self.assertFalse(profile["live_trading"])
        self.assertFalse(profile["arbitrary_code_execution"])

    async def test_legacy_client_can_use_same_contract(self) -> None:
        server = build_server(Settings(environment="test"))
        async with Client(server, mode="legacy") as client:
            result = await client.call_tool(
                "gambit_check_contract", {"contract_version": "v1"}
            )

        self.assertFalse(result.is_error)


class SettingsBoundsTests(TestCase):
    def test_local_bind_and_finite_limits_are_defaults(self) -> None:
        settings = Settings(environment="test")
        self.assertEqual(settings.host, "127.0.0.1")
        self.assertEqual(settings.max_request_body_bytes, 1_048_576)
        self.assertEqual(settings.max_response_bytes, 65_536)
        self.assertEqual(settings.max_concurrent_calls, 8)
        self.assertEqual(settings.tool_timeout_seconds, 30)

    def test_invalid_transport_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Settings(transport="sse")

    def test_http_app_has_minimal_operational_health(self) -> None:
        settings = Settings(
            environment="test", release="0.1.0", revision="test-revision"
        )
        app = build_server(settings).streamable_http_app(
            stateless_http=True,
            max_request_body_size=settings.max_request_body_bytes,
        )
        with TestClient(app) as client:
            live = client.get(
                "/health/live", headers={"x-request-id": "mcp-health-test"}
            )
            version = client.get("/health/version")
        self.assertEqual(live.json(), {"status": "ok"})
        self.assertEqual(live.headers["x-request-id"], "mcp-health-test")
        self.assertEqual(
            version.json(),
            {
                "service": "gambit-mcp",
                "environment": "test",
                "release": "0.1.0",
                "revision": "test-revision",
            },
        )

    def test_http_health_replaces_invalid_request_id(self) -> None:
        app = build_server(Settings(environment="test")).streamable_http_app(
            stateless_http=True
        )
        with TestClient(app) as client:
            response = client.get(
                "/health/live", headers={"x-request-id": "invalid request id"}
            )
        self.assertEqual(len(response.headers["x-request-id"]), 32)

    def test_http_transport_rejects_oversized_body_before_dispatch(self) -> None:
        settings = Settings(environment="test", max_request_body_bytes=1024)
        app = build_server(settings).streamable_http_app(
            stateless_http=True,
            max_request_body_size=settings.max_request_body_bytes,
        )
        with TestClient(app) as client:
            response = client.post(
                "/mcp",
                content=b"{" + (b" " * 1024) + b"}",
                headers={"content-type": "application/json"},
            )
        self.assertEqual(response.status_code, 413)
