from __future__ import annotations

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class JarvisMCPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # URL của JARVIS core API
    # service_port trong config/runtime.json là 8002
    jarvis_core_url: str = "http://localhost:8002"

    # API key nếu core bật AUTOBOT_API_KEY
    jarvis_api_key: str = ""

    # Timeout tính bằng giây cho mỗi request tới core
    jarvis_request_timeout: float = 120.0

    # Transport mode: "stdio" hoặc "sse"
    jarvis_mcp_transport: str = "stdio"


_settings: JarvisMCPSettings | None = None


def get_settings() -> JarvisMCPSettings:
    global _settings
    if _settings is None:
        _settings = JarvisMCPSettings()
    return _settings
