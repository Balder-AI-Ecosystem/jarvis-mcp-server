from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .tools import register_all_tools

mcp = FastMCP(
    name="jarvis",
    instructions=(
        "Bạn đang kết nối với JARVIS — Local Autonomous AI Ecosystem. "
        "Dùng các tool dưới đây để chat với JARVIS, xem lịch sử, "
        "kiểm tra trạng thái hệ thống, tìm kiếm kiến thức, và quản lý chu kỳ tự vận hành."
    ),
)

register_all_tools(mcp)
