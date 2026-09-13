import math
from datetime import UTC, datetime
from unittest import TestCase

from pydantic import ValidationError

from gambit_mcp.market_data import MarketDataBatch, MarketDataObservation


def _observation(day: int, *, price: float = 100.0) -> MarketDataObservation:
    return MarketDataObservation(
        timestamp=datetime(2024, 1, day, 21, tzinfo=UTC),
        price=price,
        volume=10.0,
    )


class MarketDataContractTests(TestCase):
    def test_accepts_bounded_normalized_golden_case(self) -> None:
        batch = MarketDataBatch(
            semantic_profile="gambit-market-data-v1",
            instrument="SPY",
            currency="USD",
            calendar="XNYS",
            adjustment="split-adjusted",
            observations=(_observation(2), _observation(3, price=101.0)),
        )

        self.assertEqual(len(batch.observations), 2)
        self.assertEqual(batch.instrument, "SPY")

    def test_rejects_naive_timestamp(self) -> None:
        with self.assertRaisesRegex(ValidationError, "explicit UTC offset"):
            MarketDataObservation(timestamp=datetime(2024, 1, 2), price=100.0)

    def test_rejects_non_finite_or_non_positive_prices(self) -> None:
        for price in (math.nan, math.inf, -math.inf, 0.0, -1.0):
            with (
                self.subTest(price=price),
                self.assertRaisesRegex(ValidationError, "finite and positive"),
            ):
                _observation(2, price=price)

    def test_rejects_duplicate_or_unordered_timestamps(self) -> None:
        for observations in (
            (_observation(2), _observation(2)),
            (_observation(3), _observation(2)),
        ):
            with (
                self.subTest(observations=observations),
                self.assertRaisesRegex(ValidationError, "strictly increasing"),
            ):
                MarketDataBatch(
                    semantic_profile="gambit-market-data-v1",
                    instrument="SPY",
                    currency="USD",
                    calendar="XNYS",
                    adjustment="raw",
                    observations=observations,
                )

    def test_rejects_unknown_fields_and_invalid_identifiers(self) -> None:
        with self.assertRaises(ValidationError):
            MarketDataBatch.model_validate(
                {
                    "semantic_profile": "gambit-market-data-v1",
                    "instrument": "../../SPY",
                    "currency": "usd",
                    "calendar": "XNYS",
                    "adjustment": "raw",
                    "observations": [_observation(2).model_dump()],
                    "source_url": "https://example.invalid/data",
                }
            )
