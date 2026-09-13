"""Application-owned contracts for external systems."""

from __future__ import annotations

from types import TracebackType
from typing import Protocol, Self

from .market_data import MarketDataBatch, MarketDataValidation


class GambitPort(Protocol):
    """Narrow adapter boundary; never expose Gambit's full module API."""

    def validate_market_data(self, batch: MarketDataBatch) -> MarketDataValidation:
        """Validate an already admitted normalized batch without mutating it."""
        ...


class UnitOfWork(Protocol):
    """Transaction boundary implemented by an infrastructure adapter."""

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
