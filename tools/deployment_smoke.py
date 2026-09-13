"""Verify a deployed service over its public HTTP boundary."""

from __future__ import annotations

import argparse
import uuid
from collections.abc import Sequence
from typing import cast
from urllib.parse import urlsplit

from httpx2 import Client, Response


def validate_origin(value: str, *, allow_http: bool) -> str:
    parsed = urlsplit(value)
    allowed_schemes = {"https", "http"} if allow_http else {"https"}
    if (
        parsed.scheme not in allowed_schemes
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
    ):
        raise ValueError("base URL must be a credential-free HTTPS origin")
    return value.rstrip("/")


def _get(
    client: Client, path: str, request_id: str
) -> tuple[Response, dict[str, object]]:
    response = client.get(path, headers={"x-request-id": request_id})
    if response.status_code != 200:
        raise RuntimeError(f"{path} returned HTTP {response.status_code}")
    if response.headers.get("x-request-id") != request_id:
        raise RuntimeError(f"{path} did not preserve the deployment request ID")
    raw: object = response.json()
    if not isinstance(raw, dict) or not all(isinstance(key, str) for key in raw):
        raise RuntimeError(f"{path} did not return a JSON object")
    return response, cast(dict[str, object], raw)


def verify_deployment(
    base_url: str,
    *,
    expected_service: str,
    expected_environment: str,
    expected_release: str,
    expected_revision: str,
    timeout_seconds: float = 5,
    allow_http: bool = False,
) -> None:
    origin = validate_origin(base_url, allow_http=allow_http)
    request_id = f"deployment-smoke-{uuid.uuid4().hex}"
    with Client(
        base_url=origin, timeout=timeout_seconds, follow_redirects=False
    ) as client:
        _, live = _get(client, "/health/live", request_id)
        _, ready = _get(client, "/health/ready", request_id)
        _, version = _get(client, "/health/version", request_id)

    if live != {"status": "ok"}:
        raise RuntimeError("liveness response did not match the deployment contract")
    if ready != {"status": "ready"}:
        raise RuntimeError("readiness response did not match the deployment contract")
    expected = {
        "service": expected_service,
        "environment": expected_environment,
        "release": expected_release,
        "revision": expected_revision,
    }
    if version != expected:
        raise RuntimeError(
            f"deployed identity mismatch: expected {expected}, got {version}"
        )


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--base-url", required=True)
    command.add_argument("--expected-service", required=True)
    command.add_argument("--expected-environment", required=True)
    command.add_argument("--expected-release", required=True)
    command.add_argument("--expected-revision", required=True)
    command.add_argument("--timeout-seconds", type=float, default=5)
    command.add_argument("--allow-http", action="store_true", help=argparse.SUPPRESS)
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    verify_deployment(
        args.base_url,
        expected_service=args.expected_service,
        expected_environment=args.expected_environment,
        expected_release=args.expected_release,
        expected_revision=args.expected_revision,
        timeout_seconds=args.timeout_seconds,
        allow_http=args.allow_http,
    )
    print("deployment verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
