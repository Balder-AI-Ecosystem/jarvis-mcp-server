from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from ..bridge import get_bridge


def register_chat_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def jarvis_chat(
        message: str,
        session_id: str = "",
    ) -> str:
        """Gửi tin nhắn tới JARVIS và nhận phản hồi.

        Args:
            message: Nội dung tin nhắn gửi tới JARVIS.
            session_id: (tuỳ chọn) ID phiên hội thoại để duy trì ngữ cảnh.
        """
        bridge = get_bridge()
        result = await bridge.chat(
            message=message,
            session_id=session_id or None,
        )
        reply = result.get("reply") or result.get("response") or result.get("message") or ""
        if not reply and isinstance(result, dict):
            reply = json.dumps(result, ensure_ascii=False, indent=2)
        return str(reply)

    @mcp.tool()
    async def jarvis_chat_history(limit: int = 20) -> str:
        """Lấy lịch sử hội thoại gần đây với JARVIS.

        Args:
            limit: Số lượng tin nhắn tối đa cần lấy (mặc định 20).
        """
        bridge = get_bridge()
        history = await bridge.chat_history(limit=limit)
        if not history:
            return "Chưa có lịch sử hội thoại."
        lines: list[str] = []
        for item in history:
            role = str(item.get("role") or item.get("sender") or "?").upper()
            content = str(item.get("content") or item.get("message") or item.get("text") or "")
            ts = str(item.get("timestamp") or item.get("created_at") or "")
            prefix = f"[{ts}] " if ts else ""
            lines.append(f"{prefix}{role}: {content}")
        return "\n".join(lines)
