# Хакатон-шаблоны: Skills + MCP-tools

Стартовый набор артефактов под трек «ПрокачAI PDLC» (аналитика / разработка / тестирование).
Цель — не искать структуру на самом хакатоне, а сразу подставлять свою логику.

## Структура

```
template/
├── mcp-server/        # (1) шаблон MCP-сервера: stdio + HTTP/SSE, обвязка tool-ов
├── skills/            # (2) шаблоны скиллов: базовый + примеры под 3 кейса
├── benchmark/         # мини-фреймворк замера «до/после» (баллы на защите)
├── templates/         # шаблоны артефактов: БТ, PR, маппинг тестов
├── requirements.txt
└── .env.example
```

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt
copy .env.example .env         # затем заполнить ключи
```

Запуск MCP-сервера:

```bash
# локальный (stdio) — для подключения к агенту как дочерний процесс
python mcp-server/server_stdio.py

# по HTTP/SSE — для удалённого подключения
python mcp-server/server_http.py
```

## Что менять под свой кейс

1. `mcp-server/tools/` — добавить свои tool-ы (обёртки над SberTrack/SonarQube/GitLab/TMS).
2. `skills/<твой-скилл>/SKILL.md` — описать роль агента, алгоритм, формат выхода.
3. `benchmark/benchmark_template.py` — прописать метрику кейса (время, %, полнота).
4. `templates/` — подогнать шаблоны выходных артефактов.

## Важно (уточнить у организаторов)

Формат `SKILL.md` здесь сделан по открытому стандарту Agent Skills. Если GigaCode
ожидает свой внутренний формат/каталог — поправить frontmatter и путь размещения.
