"""Owned public contracts for the initial MCP surface."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

SPEC_REVISION = "2026-07-28"
SERVER_VERSION = "0.1.0"
GAMBIT_BASELINE = "9c550bdae592e975f12046ebbb8d690889fd9206"
TEMPLATE_BASELINE = "6526db4"


class ContractCheck(BaseModel):
    """Bounded structured response for the walking-skeleton tool."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    accepted: Literal[True] = True
    contract_version: Literal["v1"] = "v1"
    server_version: str = SERVER_VERSION
    target_spec_revision: str = SPEC_REVISION
    scope: Literal["read-only-research"] = "read-only-research"


class ServerProfile(BaseModel):
    """Machine-readable server identity and safety boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    server: Literal["gambit-mcp"] = "gambit-mcp"
    server_version: str = SERVER_VERSION
    target_spec_revision: str = SPEC_REVISION
    gambit_baseline: str = GAMBIT_BASELINE
    template_baseline: str = TEMPLATE_BASELINE
    maturity: Literal["walking-skeleton"] = "walking-skeleton"
    scope: Literal["read-only-research"] = "read-only-research"
    live_trading: Literal[False] = False
    arbitrary_code_execution: Literal[False] = False


class CapabilityProfile(BaseModel):
    """Current implemented and deliberately unavailable capabilities."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    implemented_tools: tuple[str, ...] = ("gambit_check_contract",)
    implemented_resources: tuple[str, ...] = (
        "gambit://server/about",
        "gambit://capabilities",
    )
    unavailable_until_approved: tuple[str, ...] = (
        "market_data_validation",
        "dataset_registration",
        "backtest_execution",
        "result_storage",
        "live_trading",
    )
