from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from ..bridge import get_bridge


def register_memory_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def jarvis_knowledge_search(
        query: str,
        lane: str = "",
        top_k: int = 5,
    ) -> str:
        """Tìm kiếm kiến thức trong External Brain của JARVIS.

        Args:
            query: Câu truy vấn tìm kiếm.
            lane: (tuỳ chọn) Lọc theo zone/lane — "user_brain" hoặc "procedural_brain".
                  Để trống để tìm trong tất cả lane.
            top_k: Số kết quả tối đa trả về (mặc định 5).
        """
        bridge = get_bridge()
        # Returns list of {path, zone, source, score}
        hits = await bridge.knowledge_search(
            query=query,
            lane=lane or None,
            top_k=top_k,
        )
        if not hits:
            return f"Không tìm thấy kết quả nào cho: {query!r}"
        lines: list[str] = []
        for i, hit in enumerate(hits, start=1):
            path = str(hit.get("path") or "")
            zone = str(hit.get("zone") or "")
            source = str(hit.get("source") or "")
            score = hit.get("score")
            score_str = f" (score={score:.3f})" if isinstance(score, float) else ""
            meta = f"[{zone}|{source}]" if zone or source else ""
            lines.append(f"{i}. {meta}{score_str} {path}")
        return "\n".join(lines)
