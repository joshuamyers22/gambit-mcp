"""Exercise the built container over a real socket and verify its runtime user."""

from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.request

from deployment_smoke import verify_deployment

CONTAINER = "gambit-mcp-smoke"
IMAGE = "gambit-mcp:local"


def main() -> int:
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--name",
            CONTAINER,
            "-d",
            "-p",
            "127.0.0.1:18080:8000",
            IMAGE,
        ],
        check=True,
    )
    try:
        for attempt in range(10):
            try:
                request = urllib.request.Request(
                    "http://127.0.0.1:18080/health/live",
                    headers={"x-request-id": "container-smoke"},
                )
                with urllib.request.urlopen(request, timeout=2) as response:
                    payload = json.load(response)
                    assert response.status == 200
                    assert response.headers["x-request-id"] == "container-smoke"
                    assert payload == {"status": "ok"}
                break
            except OSError:
                if attempt == 9:
                    raise
                time.sleep(1)
        user = subprocess.run(
            ["docker", "inspect", "--format", "{{.Config.User}}", CONTAINER],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if user != "10001:10001":
            raise RuntimeError(f"unexpected container user: {user!r}")
        labels_raw = subprocess.run(
            ["docker", "inspect", "--format", "{{json .Config.Labels}}", CONTAINER],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        labels: object = json.loads(labels_raw)
        expected_labels = {
            "org.opencontainers.image.version": os.environ.get("APP_RELEASE", "0.1.0"),
            "org.opencontainers.image.revision": os.environ.get(
                "APP_REVISION", "local"
            ),
        }
        if not isinstance(labels, dict) or any(
            labels.get(key) != value for key, value in expected_labels.items()
        ):
            raise RuntimeError(f"unexpected image identity labels: {labels!r}")
        verify_deployment(
            "http://127.0.0.1:18080",
            expected_service="gambit-mcp",
            expected_environment="development",
            expected_release=os.environ.get("APP_RELEASE", "0.1.0"),
            expected_revision=os.environ.get("APP_REVISION", "local"),
            allow_http=True,
        )
    finally:
        subprocess.run(["docker", "stop", CONTAINER], check=False)
    print("container smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
