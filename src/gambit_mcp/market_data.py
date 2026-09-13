"""Owned, parser-independent market-data admission contracts for M2."""

from __future__ import annotations

import math
from datetime import datetime
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

InstrumentId = Annotated[str, StringConstraints(pattern=r"^[A-Z0-9][A-Z0-9._-]{0,31}$")]
Currency = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]


class MarketDataObservation(BaseModel):
    """One normalized observation; parsers must produce this owned shape."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    timestamp: datetime
    price: float
    volume: float | None = None

    @model_validator(mode="after")
    def validate_values(self) -> Self:
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must include an explicit UTC offset")
        if not math.isfinite(self.price) or self.price <= 0:
            raise ValueError("price must be finite and positive")
        if self.volume is not None and (
            not math.isfinite(self.volume) or self.volume < 0
        ):
            raise ValueError("volume must be finite and non-negative")
        return self


class MarketDataBatch(BaseModel):
    """Bounded normalized batch independent of Arrow, Polars, and Gambit."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    semantic_profile: Literal["gambit-market-data-v1"]
    instrument: InstrumentId
    currency: Currency
    calendar: Annotated[str, StringConstraints(pattern=r"^[A-Z0-9._-]{1,32}$")]
    adjustment: Literal["raw", "split-adjusted", "total-return"]
    observations: Annotated[
        tuple[MarketDataObservation, ...], Field(min_length=1, max_length=10_000)
    ]

    @model_validator(mode="after")
    def require_ordered_unique_timestamps(self) -> Self:
        timestamps = [item.timestamp for item in self.observations]
        if any(
            current <= previous
            for previous, current in zip(timestamps, timestamps[1:], strict=False)
        ):
            raise ValueError("timestamps must be strictly increasing and unique")
        return self


class MarketDataFinding(BaseModel):
    """Stable project-owned validation finding."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]{0,63}$")]
    severity: Literal["error", "warning"]
    count: int = Field(ge=0)


class MarketDataValidation(BaseModel):
    """Separate structural validity from financial qualification."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    well_formed: bool
    financially_qualified: bool
    findings: Annotated[tuple[MarketDataFinding, ...], Field(max_length=128)] = ()
    gambit_version: Annotated[str, StringConstraints(min_length=1, max_length=64)]
