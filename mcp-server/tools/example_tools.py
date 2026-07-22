"""Набор tool-ов для MCP-сервера.

Здесь регистрируются все инструменты, которые агент сможет вызывать.
`register_tools(mcp)` подключается и в stdio-, и в http-варианте сервера,
чтобы не дублировать логику.

Замени примеры ниже на обёртки над реальными системами
(SberTrack / SonarQube / GitLab / TMS).
"""
from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx


# --------------------------------------------------------------------------- #
# Вспомогательное: HTTP-запрос с ретраями и внятной обработкой ошибок.
# Используй это в своих tool-ах, чтобы не падать на первой сетевой ошибке.
# --------------------------------------------------------------------------- #
async def http_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: Any | None = None,
    retries: int = 3,
    backoff: float = 0.5,
    timeout: float = 20.0,
) -> dict[str, Any]:
    """Единая точка для внешних вызовов: ретраи + читаемые ошибки.

    Возвращает dict: {"ok": bool, "status": int, "data": ..., "error": ...}
    Не бросает исключение наружу — агент получит структурированный результат
    и сможет сам решить, что делать.
    """
    last_error: str | None = None
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(1, retries + 1):
            try:
                resp = await client.request(
                    method.upper(), url, headers=headers, params=params, json=json_body
                )
                resp.raise_for_status()
                try:
                    data: Any = resp.json()
                except ValueError:
                    data = resp.text
                return {"ok": True, "status": resp.status_code, "data": data, "error": None}
            except httpx.HTTPStatusError as exc:
                # 4xx обычно нет смысла ретраить (кроме 429)
                status = exc.response.status_code
                last_error = f"HTTP {status}: {exc.response.text[:500]}"
                if status < 500 and status != 429:
                    break
            except (httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout) as exc:
                last_error = f"{type(exc).__name__}: {exc}"

            if attempt < retries:
                await asyncio.sleep(backoff * attempt)

    return {"ok": False, "status": 0, "data": None, "error": last_error}


# --------------------------------------------------------------------------- #
# Регистрация tool-ов.
# --------------------------------------------------------------------------- #
def register_tools(mcp) -> None:
    """Регистрирует все tool-ы на переданном экземпляре FastMCP."""

    @mcp.tool()
    async def echo(text: str) -> str:
        """Проверочный tool. Возвращает переданный текст.

        Используй для проверки, что сервер поднялся и агент видит инструменты.
        """
        return text

    @mcp.tool()
    async def fetch_url(url: str) -> dict[str, Any]:
        """Делает GET-запрос по URL и возвращает результат.

        Пример tool-а «наружу». В реальном кейсе замени на вызов
        конкретного API (например, получить issues из SonarQube).

        Args:
            url: полный URL для запроса.
        """
        return await http_request("GET", url)

    # -------- Заготовка под реальную систему (раскомментируй и заполни) ----- #
    # @mcp.tool()
    # async def create_bt(title: str, description: str) -> dict[str, Any]:
    #     """Создаёт бизнес-требование (БТ) в SberTrack."""
    #     base = os.environ["SBERTRACK_BASE_URL"]
    #     token = os.environ["SBERTRACK_TOKEN"]
    #     return await http_request(
    #         "POST",
    #         f"{base}/api/v1/issues",
    #         headers={"Authorization": f"Bearer {token}"},
    #         json_body={"title": title, "description": description},
    #     )
