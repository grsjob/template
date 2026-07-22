"""MCP-сервер, вариант stdio (локальный).

Агент запускает этот файл как дочерний процесс и общается по stdin/stdout.
Подходит для локальной разработки и подключения к кодовому агенту на своей машине.

Запуск вручную (для проверки):
    python mcp-server/server_stdio.py

Подключение в конфиге агента (пример):
    {
      "command": "python",
      "args": ["D:/web/template/mcp-server/server_stdio.py"],
      "transport": "stdio"
    }
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# tools/ лежит рядом — добавим папку сервера в путь импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import register_tools  # noqa: E402

load_dotenv()

mcp = FastMCP("hackathon-mcp")
register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")
