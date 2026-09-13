"""Minimal structured logging without application-data leakage."""

from __future__ import annotations

import json
import logging
import math
import re
from datetime import UTC, datetime

SEVERITIES = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
OUTCOMES = {"success", "rejected", "error", "degraded", "cancelled"}
EVENT_NAME = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")
OPERATION_NAME = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
ERROR_CODE = re.compile(r"^[A-Z][A-Z0-9_]*$")
OPTIONAL_FIELDS = (
    "correlation_id",
    "duration_ms",
    "error_code",
    "error_type",
    "retryable",
    "http_method",
    "http_route",
    "http_status",
)


class JsonFormatter(logging.Formatter):
    def __init__(self, context: dict[str, str]) -> None:
        super().__init__()
        self.context = context

    def format(self, record: logging.LogRecord) -> str:
        severity = record.levelname if record.levelname in SEVERITIES else "INFO"
        event = getattr(record, "event", "application_logged")
        if not isinstance(event, str) or EVENT_NAME.fullmatch(event) is None:
            event = "telemetry_contract_rejected"
        operation = getattr(record, "operation", record.name)
        if (
            not isinstance(operation, str)
            or len(operation) > 128
            or OPERATION_NAME.fullmatch(operation) is None
        ):
            operation = "application"
        outcome = getattr(
            record,
            "outcome",
            "error" if record.levelno >= logging.ERROR else "success",
        )
        if outcome not in OUTCOMES:
            outcome = "error"
        if outcome == "error" and severity not in {"ERROR", "CRITICAL"}:
            severity = "ERROR"
        payload = {
            "schema_version": 1,
            "timestamp": datetime.now(UTC).isoformat(),
            "severity": severity,
            "event": event,
            "operation": operation,
            "outcome": outcome,
            **self.context,
        }
        if getattr(record, "safe_message", False):
            payload["message"] = record.getMessage()[:1024]
        optional: dict[str, object] = {}
        for key in OPTIONAL_FIELDS:
            value = getattr(record, key, None)
            if value is not None and self._valid_optional(key, value):
                optional[key] = value
        error_present = any(
            key in optional for key in ("error_code", "error_type", "retryable")
        )
        if outcome == "error" or error_present:
            code = optional.get("error_code", "UNCLASSIFIED_ERROR")
            error_type = optional.get("error_type", "UnclassifiedError")
            retryable = optional.get("retryable", False)
            optional.update(
                {
                    "error_code": code,
                    "error_type": error_type,
                    "retryable": retryable,
                }
            )
        payload.update(optional)
        return json.dumps(payload, separators=(",", ":"), sort_keys=True)

    @staticmethod
    def _valid_optional(key: str, value: object) -> bool:
        if key == "correlation_id":
            return isinstance(value, str) and 1 <= len(value) <= 128
        if key == "duration_ms":
            return (
                isinstance(value, int | float)
                and not isinstance(value, bool)
                and math.isfinite(value)
                and value >= 0
            )
        if key == "error_code":
            return (
                isinstance(value, str)
                and len(value) <= 128
                and ERROR_CODE.fullmatch(value) is not None
            )
        if key == "error_type":
            return isinstance(value, str) and 1 <= len(value) <= 128
        if key == "retryable":
            return isinstance(value, bool)
        if key == "http_method":
            return isinstance(value, str) and len(value) <= 16
        if key == "http_route":
            return isinstance(value, str) and len(value) <= 256
        if key == "http_status":
            return (
                isinstance(value, int)
                and not isinstance(value, bool)
                and 100 <= value <= 599
            )
        return False


def configure_logging(
    level: str, *, service: str, environment: str, release: str, revision: str
) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(
        JsonFormatter(
            {
                "service": service,
                "environment": environment,
                "release": release,
                "revision": revision,
            }
        )
    )
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level.upper())
