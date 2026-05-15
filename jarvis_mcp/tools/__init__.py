from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .chat import register_chat_tools
from .autonomy import register_autonomy_tools
from .memory import register_memory_tools
from .runtime import register_runtime_tools

__all__ = [
    "register_chat_tools",
    "register_autonomy_tools",
    "register_memory_tools",
    "register_runtime_tools",
]


def register_all_tools(mcp: FastMCP) -> None:
    register_chat_tools(mcp)
    register_autonomy_tools(mcp)
    register_memory_tools(mcp)
    register_runtime_tools(mcp)
