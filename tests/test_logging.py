import json
import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Protocol, cast
from unittest import TestCase

from jsonschema import Draft202012Validator, FormatChecker

from gambit_mcp.logging import JsonFormatter


class Validator(Protocol):
    def iter_errors(self, instance: object) -> Iterable[object]: ...


class LoggingContractTests(TestCase):
    def test_structured_event_matches_schema_and_drops_unknown_fields(self) -> None:
        formatter = JsonFormatter(
            {
                "service": "gambit-mcp",
                "environment": "test",
                "release": "0.1.0",
                "revision": "test-revision",
            }
        )
        record = logging.LogRecord("test", logging.INFO, __file__, 1, "ok", (), None)
        record.event = "contract_checked"  # type: ignore[attr-defined]
        record.operation = "mcp.gambit_check_contract"  # type: ignore[attr-defined]
        record.outcome = "success"  # type: ignore[attr-defined]
        record.secret = "must-not-appear"  # type: ignore[attr-defined]
        payload_text = formatter.format(record)
        payload = json.loads(payload_text)

        schema = json.loads(
            (
                Path(__file__).resolve().parents[1]
                / "schemas"
                / "telemetry-event.schema.json"
            ).read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        validator = cast(
            Validator,
            Draft202012Validator(schema, format_checker=FormatChecker()),
        )
        self.assertEqual(list(validator.iter_errors(payload)), [])
        self.assertNotIn("must-not-appear", payload_text)

    def test_unsafe_message_is_not_emitted(self) -> None:
        formatter = JsonFormatter(
            {
                "service": "gambit-mcp",
                "environment": "test",
                "release": "0.1.0",
                "revision": "test-revision",
            }
        )
        record = logging.LogRecord(
            "test", logging.ERROR, __file__, 1, "sensitive payload", (), None
        )
        payload = json.loads(formatter.format(record))
        self.assertNotIn("message", payload)
        self.assertEqual(payload["error_code"], "UNCLASSIFIED_ERROR")
