"""MCP-сервер, вариант HTTP/SSE (удалённый).

Поднимает сетевой эндпоинт, к которому агент подключается по HTTP.
Подходит, когда сервер крутится отдельно (контейнер / удалённая машина).

Запуск:
    python mcp-server/server_http.py

Хост/порт берутся из .env (MCP_HTTP_HOST / MCP_HTTP_PORT).

Подключение в конфиге агента (пример):
    {
      "url": "http://127.0.0.1:8000/sse",
      "transport": "sse"
    }
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import register_tools  # noqa: E402

load_dotenv()

host = os.environ.get("MCP_HTTP_HOST", "127.0.0.1")
port = int(os.environ.get("MCP_HTTP_PORT", "8000"))

mcp = FastMCP("hackathon-mcp", host=host, port=port)
register_tools(mcp)


if __name__ == "__main__":
    # transport="sse" отдаёт эндпоинт /sse; при желании можно
    # использовать "streamable-http" (эндпоинт /mcp) в свежих версиях SDK.
    mcp.run(transport="sse")
