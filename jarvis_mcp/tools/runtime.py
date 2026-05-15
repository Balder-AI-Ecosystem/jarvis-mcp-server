from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from ..bridge import get_bridge


def register_runtime_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def jarvis_health() -> str:
        """Kiểm tra trạng thái sức khoẻ của JARVIS core API."""
        bridge = get_bridge()
        result = await bridge.health()
        status = str(result.get("status") or "unknown")
        details = {k: v for k, v in result.items() if k != "status"}
        lines = [f"Status: {status}"]
        if details:
            lines.append(json.dumps(details, ensure_ascii=False, indent=2))
        return "\n".join(lines)

    @mcp.tool()
    async def jarvis_runtime_preflight() -> str:
        """Chạy kiểm tra preflight hệ thống JARVIS: model availability, config, dependencies."""
        bridge = get_bridge()
        result = await bridge.runtime_preflight()
        checks = result.get("checks") or result.get("results") or result
        if isinstance(checks, dict):
            lines: list[str] = []
            for key, val in checks.items():
                status = str(val.get("status") or val) if isinstance(val, dict) else str(val)
                detail = val.get("detail") or "" if isinstance(val, dict) else ""
                suffix = f" — {detail}" if detail else ""
                lines.append(f"{key}: {status}{suffix}")
            return "\n".join(lines) if lines else "Preflight passed."
        return json.dumps(result, ensure_ascii=False, indent=2)
