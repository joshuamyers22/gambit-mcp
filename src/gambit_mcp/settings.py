"""Validated environment configuration."""

from __future__ import annotations

from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")

    environment: str = Field(
        default="development",
        pattern=r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$",
        max_length=64,
    )
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "info"
    release: str = Field(default="0.1.0", min_length=1, max_length=128)
    revision: str = Field(default="local", min_length=1, max_length=128)
    graceful_shutdown_seconds: int = Field(default=30, ge=1, le=300)
    transport: str = Field(default="stdio", pattern=r"^(stdio|streamable-http)$")
    mcp_path: str = Field(default="/mcp", pattern=r"^/[A-Za-z0-9/_-]*$")
    max_request_body_bytes: int = Field(default=1_048_576, ge=1024, le=4_194_304)
    max_response_bytes: int = Field(default=65_536, ge=1024, le=1_048_576)
    max_concurrent_calls: int = Field(default=8, ge=1, le=1024)
    tool_timeout_seconds: int = Field(default=30, ge=1, le=300)

    @model_validator(mode="after")
    def require_production_identity(self) -> Self:
        if self.environment.casefold() == "production" and self.revision.casefold() in {
            "local",
            "unknown",
        }:
            raise ValueError(
                "APP_REVISION must identify the deployed commit in production"
            )
        return self
