from __future__ import annotations

from .server import mcp
from .config import get_settings


def main() -> None:
    settings = get_settings()
    transport = str(settings.jarvis_mcp_transport or "stdio").strip().lower()
    mcp.run(transport=transport)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
