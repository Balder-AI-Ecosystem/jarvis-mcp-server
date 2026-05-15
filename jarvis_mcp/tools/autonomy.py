from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from ..bridge import get_bridge


def register_autonomy_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def jarvis_autonomy_status() -> str:
        """Xem trạng thái hiện tại của chu kỳ tự vận hành (autonomy cycle) của JARVIS."""
        bridge = get_bridge()
        status = await bridge.autonomy_status()
        return json.dumps(status, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def jarvis_autonomy_run(
        goals: str = "",
        allow_promotion: bool = True,
    ) -> str:
        """Kích hoạt thủ công một chu kỳ tự vận hành (research / self-audit / upgrade).

        Args:
            goals: (tuỳ chọn) Danh sách mục tiêu cách nhau bằng dấu phẩy.
                   Để trống để dùng default policy của JARVIS.
            allow_promotion: Cho phép promote kết quả vào External Brain (mặc định True).
        """
        bridge = get_bridge()
        goals_list = [g.strip() for g in goals.split(",") if g.strip()] if goals else None
        result = await bridge.autonomy_run(
            goals=goals_list,
            allow_promotion=allow_promotion,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def jarvis_autonomy_lifecycle(limit: int = 10) -> str:
        """Xem lịch sử các chu kỳ tự vận hành gần đây.

        Args:
            limit: Số lượng bản ghi cần lấy (mặc định 10).
        """
        bridge = get_bridge()
        records = await bridge.autonomy_lifecycle(limit=limit)
        if not records:
            return "Chưa có lịch sử autonomy cycle."
        lines: list[str] = []
        for record in records:
            ts = str(record.get("timestamp") or record.get("created_at") or "")
            path = str(record.get("path") or record.get("cycle_path") or "")
            status = str(record.get("status") or record.get("result") or "")
            lines.append(f"[{ts}] path={path} status={status}")
        return "\n".join(lines)
